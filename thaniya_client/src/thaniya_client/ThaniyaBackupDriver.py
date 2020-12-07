

import re
import os
import typing
import time
import datetime
import json
import sys
import shutil

import jk_typing
import jk_utils
import jk_mounting
import jk_logging
from jk_testing import Assert
import jk_json

from .constants import *
from .TargetDirectoryStrategy_StaticDir import TargetDirectoryStrategy_StaticDir
from .AbstractBackupConnector import AbstractBackupConnector
from .ThaniyaBackupContext import ThaniyaBackupContext
from .ThaniyaIO import ThaniyaIO
from .ProcessingFallThroughError import ProcessingFallThroughError
from .ProcessingContext import ProcessingContext
from .AbstractTargetDirectoryStrategy import AbstractTargetDirectoryStrategy
from .ThaniyaBackupStats import ThaniyaBackupStats
from .tasks.AbstractThaniyaTask import AbstractThaniyaTask
from .BD2 import BD2





class ThaniyaBackupDriver(object):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	#
	# Constructor method.
	#
	# @param	AbstractBackupConnector backupConnector				An object that is used to connect to a backup repository/backup server later.
	# @param	dict backupConnectorParameters						A dictionary that holds various parameters required to connect to the backup repository/backup server.
	# @param	AbstractTargetDirectoryStrategy targetDirStrategy	A strategy that decides about which target directory to use exactly.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self,
		backupConnector:AbstractBackupConnector,
		backupConnectorParameters:dict,
		targetDirStrategy:typing.Union[AbstractTargetDirectoryStrategy,None] = None,
		):

		self.__targetDirStrategy = None			# AbstractTargetDirectoryStrategy
		self.__backupConnector = None			# AbstractBackupConnector
		self.__backupConnectorParameters = None	# dict

		self.__setTargetDirStrategy(targetDirStrategy)
		self.__setConnector(backupConnector, backupConnectorParameters)
	#

	################################################################################################################################
	## Low Level Helper Methods
	################################################################################################################################

	#
	# This method is invoked by <c>__init__()</c>.
	#
	def __setTargetDirStrategy(self, targetDirStrategy:typing.Union[AbstractTargetDirectoryStrategy,None]):
		if targetDirStrategy is None:
			targetDirStrategy = TargetDirectoryStrategy_StaticDir()
		else:
			assert isinstance(targetDirStrategy, AbstractTargetDirectoryStrategy)

		self.__targetDirStrategy = targetDirStrategy
	#

	#
	# This method is invoked by <c>__init__()</c>.
	#
	def __setConnector(self, backupConnector:AbstractBackupConnector, backupConnectorParameters:dict = None):
		assert isinstance(backupConnector, AbstractBackupConnector)

		if backupConnectorParameters is None:
			backupConnectorParameters = {}
		else:
			assert isinstance(backupConnectorParameters, dict)

		if backupConnector.needsToBeRoot:
			if os.geteuid() != 0:
				raise Exception("Need to be root to use backup connector " + repr(backupConnector.__class__.__name__) + "!")

		self.__backupConnector = backupConnector
		self.__backupConnectorParameters = backupConnectorParameters
	#

	################################################################################################################################

	#
	# This method is invoked by <c>__perform_deinitialize()</c>.
	#
	@jk_typing.checkFunctionSignature()
	def __writeLogToFiles(self,
		bufferLogger:jk_logging.BufferLogger,
		effectiveTargetDirPath:str,
		fileMode:typing.Union[int,str,jk_utils.ChModValue,None],
		log:jk_logging.AbstractLogger,
		):

		# TODO: use safe writing mechanisms provided by jk_utils

		textFilePath = os.path.join(effectiveTargetDirPath, PLAINTEXT_LOG_FILE_NAME)
		textFilePathTemp = textFilePath + ".tmp"
		jsonFilePath = os.path.join(effectiveTargetDirPath, JSON_LOG_FILE_NAME)
		jsonFilePathTemp = jsonFilePath + ".tmp"

		jsonLogData = bufferLogger.getDataAsPrettyJSON()

		log.notice("Writing to: " + textFilePath)
		log.notice("Writing to: " + jsonFilePath)

		bAppendToExistingFile = False
		logMsgFormatter = None

		# ----

		with open(jsonFilePathTemp, "w") as f:
			json.dump(jsonLogData, f, indent="\t")
		if fileMode is not None:
			os.chmod(jsonFilePathTemp, fileMode.toInt())
		os.rename(jsonFilePathTemp, jsonFilePath)

		# ----

		fileLogger = jk_logging.FileLogger.create(
			textFilePathTemp,
			"none",
			bAppendToExistingFile,
			False,
			fileMode,
			logMsgFormatter,

		)
		bufferLogger.forwardTo(fileLogger)
		fileLogger.close()
		if fileMode is not None:
			os.chmod(textFilePathTemp, fileMode.toInt())
		os.rename(textFilePathTemp, textFilePath)
	#

	#
	# This method is invoked by <c>testConnector()</c> and  <c>performBackup()</c>.
	#
	@jk_typing.checkFunctionSignature()
	def __checkBackupIdentifierE(self, backupIdentifier:str):
		if re.match("^[a-zA-Z_\.\-+\(\)\[\]\{\}]+$", backupIdentifier):
			return
		raise Exception("Invalid backup identifier specified: " + repr(backupIdentifier))
	#

	#
	# This method is invoked by <c>__perform_initialize()</c>.
	#
	@jk_typing.checkFunctionSignature()
	def __buildAndCheckEffectiveTargetDirPath(self, ctx:ThaniyaBackupContext, bd2:BD2, bSimulate:bool, bAllowOverwriteOldBackup:bool = True) -> str:
		# select the target directory where we will store the data. the variable "effectiveTargetDirPath"
		# will receive the directory selected by the target directory strategy. we will write data there.

		with ctx.descend("Selecting target directory") as ctx2:
			sTmp = self.__targetDirStrategy.selectEffectiveTargetDirectory(bd2)
			assert isinstance(sTmp, str)
			if sTmp:
				assert sTmp[0] not in [ "/", "\\", "." ]
				assert not os.path.isabs(sTmp)
				effectiveTargetDirPath = os.path.join(self.__backupConnector.baseTargetDirPath, sTmp)
			else:
				effectiveTargetDirPath = self.__backupConnector.baseTargetDirPath
			ctx.log.notice("Selected target directory: " + repr(effectiveTargetDirPath))
			
			# verify that we have the correct directory: the "effectiveTargetDirPath" must be located somewhere within
			# the mounted directory tree.

			if effectiveTargetDirPath.endswith("/"):
				effectiveTargetDirPath2 = effectiveTargetDirPath
			else:
				effectiveTargetDirPath2 = effectiveTargetDirPath + "/"
			assert effectiveTargetDirPath2.startswith(self.__backupConnector.baseTargetDirPath2)

			# check that the target directory fits our requirements: it must be empty.

			if os.path.isdir(effectiveTargetDirPath):
				bIsEmpty, contentEntries = ThaniyaIO.checkIfDirIsEmpty(ctx2, effectiveTargetDirPath)
				if not bIsEmpty:
					if STATS_JSON_FILE_NAME in contentEntries:
						# target directory already seems to contain a backup 
						ctx2.log.warn("Target directory already seems to contain a backup: " + effectiveTargetDirPath2)
						if not bSimulate:
							if bAllowOverwriteOldBackup:
								ctx2.log.warn("Overwriting this backup.")
							else:
								raise Exception("Target directory already seems to contain a backup: " + effectiveTargetDirPath2)
					else:
						raise Exception("Backup directory contains various non-backup files or directories!")

		# ----

		return effectiveTargetDirPath
	#

	################################################################################################################################
	## High Level Helper Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __perform_calcDiskSpaceRequired(self, bd2:BD2, backupTasks:typing.List[AbstractThaniyaTask]) -> int:
		with ProcessingContext(
			text="Calculating disk space required",
			bd2=bd2,
			bMeasureDuration=True,
			statsDurationKey="d0_calcDiskSpace"
		) as ctx:
			nExpectedBytesToWrite = 0
			for job in backupTasks:
				#assert isinstance(job, AbstractThaniyaTask)
				Assert.isInstance(job, AbstractThaniyaTask)

				nestedCtx = ctx.descend(job.logMessageCalculateSpaceRequired)
				with nestedCtx.log as nestedLog:
					nExpectedBytesToWrite += job.calculateSpaceRequired(nestedCtx)

			ctx.log.info("Estimated total size of backup: " + jk_utils.formatBytes(nExpectedBytesToWrite))

			bd2.statsContainer.setValue("expectedBytesToWrite", nExpectedBytesToWrite)

			# ----

			ctx.log.notice("Done.")

		return nExpectedBytesToWrite
	#

	@jk_typing.checkFunctionSignature()
	def __perform_initialize(self, bd2:BD2, nExpectedBytesToWrite:typing.Union[int, None]):
		with ProcessingContext(
			text="Connecting to backup repository and preparing backup",
			bd2=bd2,
			bMeasureDuration=True,
			statsDurationKey="d1_connectAndPrepare"
		) as ctx:
			# mount the remote file system

			if nExpectedBytesToWrite is None:
				nExpectedBytesToWrite = 1024

			with ctx.descend("Initializinig connection ...") as ctx2:
				self.__backupConnector.initialize(ctx2, nExpectedBytesToWrite, self.__backupConnectorParameters)

			if self.__backupConnector.performsMountUnmount:
				# connector performs mounting and unmounting
				assert self.__backupConnector.mountDirPath is not None
				# remember mount path
				bd2.mountDirPath = self.__backupConnector.mountDirPath
			else:
				# no mounting -> mount directory should be None
				assert self.__backupConnector.mountDirPath is None

			assert self.__backupConnector.baseTargetDirPath is not None
			bd2.baseTargetDirPath = self.__backupConnector.baseTargetDirPath

			if not self.__backupConnector.isReady:
				raise Exception("Backup connector unexpectedly not ready for writing!")

			# select the target directory where we will store the data. the variable "effectiveTargetDirPath"
			# will receive the directory selected by the target directory strategy. we will write data there.
			# verify that we have the correct directory: the "effectiveTargetDirPath" must be located somewhere within
			# the mounted directory tree.
			# check that the target directory fits our requirements: it must be empty.

			bd2.effectiveTargetDirPath = self.__buildAndCheckEffectiveTargetDirPath(ctx, bd2, True)

			# ensure that the directory exists

			ThaniyaIO.ensureDirExists(ctx, bd2.effectiveTargetDirPath, jk_utils.ChModValue("rwx------"))

			# now we are ready. but before we begin doing something let's write the backup stats first.

			filePath = os.path.join(bd2.effectiveTargetDirPath, STATS_JSON_FILE_NAME)
			ctx.log.notice("Writing to: " + filePath)
			bd2.statsContainer.writeToFile(filePath)

			# ----

			ctx.log.notice("Done.")
	#

	@jk_typing.checkFunctionSignature()
	def __perform_backup(self, bd2:BD2, backupTasks:typing.List[AbstractThaniyaTask]):

		# NOTE: we need to access this context later as it calculates the duration and we need this information separately to log it.
		processingContext = ProcessingContext(
			text="Writing the backup data",
			bd2=bd2,
			bMeasureDuration=True,
			statsDurationKey="d2_backup"
		)

		with processingContext as ctx:

			for job in backupTasks:
				Assert.isInstance(job, AbstractThaniyaTask)

				with ctx.descend(job.logMessagePerformBackup) as nestedCtx:
					job.performBackup(nestedCtx)

			ctx.log.notice("All backup tasks completed.")

			# calculate statistics

			with ctx.log.descend("Calculating size of backup performed ...") as nestedLog:
				nTotalBytesWritten = jk_utils.fsutils.getFolderSize(bd2.effectiveTargetDirPath)

			fDuration = processingContext.duration
			if (nTotalBytesWritten > 0) and (fDuration > 0):
				fAvgWritingSpeed = nTotalBytesWritten/fDuration
				sAvgWritingSpeed = jk_utils.formatBytesPerSecond(fAvgWritingSpeed)
			else:
				fAvgWritingSpeed = None
				sAvgWritingSpeed = "n/a"

			ctx.log.info("Total bytes written: " + jk_utils.formatBytes(nTotalBytesWritten))
			ctx.log.info("Average writing speed: " + sAvgWritingSpeed)

			bd2.statsContainer.setValue("totalBytesWritten", nTotalBytesWritten)
			bd2.statsContainer.setValue("avgWritingSpeed", fAvgWritingSpeed)

			# ----

			ctx.log.notice("Done.")
	#

	@jk_typing.checkFunctionSignature()
	def __perform_finalizeBackup(self, bd2:BD2):
		with ProcessingContext(
			text="Finalizing backup",
			bd2=bd2,
			bMeasureDuration=False,
			statsDurationKey=None
		) as ctx:

			# detecting errors

			bHasError = bd2.hasError
			bHasWarning = bd2.hasWarning

			# storing final data

			bd2.statsContainer.setValue("tEnd", time.time())
			bd2.statsContainer.setValue("bSuccess", not bHasError)

			# writing final status log message

			if bHasError:
				ctx.log.error("Backup terminated with errors.")
			else:
				if bHasWarning:
					ctx.log.warning("There were warnings!")
				ctx.log.success("Backup successfully completed.")

			# let's try to write the backup stats before termination.

			if bd2.effectiveTargetDirPath is not None:
				with ctx.descend("Writing stats ...") as ctx2:
					filePath = os.path.join(bd2.effectiveTargetDirPath, STATS_JSON_FILE_NAME)
					ctx2.log.notice("Writing to: " + filePath)
					bd2.statsContainer.writeToFile(filePath)

			# let's try to write the backup log before termination.

			if bd2.effectiveTargetDirPath is not None:
				with ctx.descend("Writing log ...") as ctx2:
					self.__writeLogToFiles(bd2.blog, bd2.effectiveTargetDirPath, None, ctx2.log)

			# ----

			ctx.log.notice("Done.")
	#

	@jk_typing.checkFunctionSignature()
	def __perform_deinitialize(self, bd2:BD2):
		with ProcessingContext(
			text="Disconnecting and cleaning up",
			bd2=bd2,
			bMeasureDuration=False,
			statsDurationKey=None
		) as ctx:
			mountDirPath = None
			mounter = None
			if self.__backupConnector.performsMountUnmount:
				mountDirPath = self.__backupConnector.mountDirPath
				mounter = jk_mounting.Mounter()
				assert mounter.isMounted(mountDirPath)

			# terminate connection

			with ctx.descend("Terminating connection ...") as ctx2:
				self.__backupConnector.deinitialize(ctx2)

			# verify that a mounted directory has been unmounted as expected

			if bd2.mountDirPath:
				mounter.refresh()
				if mounter.isMounted(bd2.mountDirPath):
					ctx.log.error("DEINITIALIZATION FAILED! Directory is still mounted: " + bd2.mountDirPath)
					ctx.log.error("This is a bug! Please contact bugs@binary-overflow.de and report this bug!")

			#try:
				#if self.__backupConnector.performsMountUnmount:
				#	ThaniyaIO.removeEmptyDir(ctx, self.__mountDirPath)
			#except Exception as ee:
			#	bError = True

			# ----

			ctx.log.notice("Done.")
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Perform a test of the connector.
	#
	@jk_typing.checkFunctionSignature()
	def testConnector(self,
		backupIdentifier:str
		) -> bool:

		self.__checkBackupIdentifierE(backupIdentifier)

		mainLog = jk_logging.ConsoleLogger.create(logMsgFormatter=jk_logging.COLOR_LOG_MESSAGE_FORMATTER)

		with BD2(backupIdentifier, mainLog) as bd2:

			try:

				self.__perform_initialize(bd2, None)
				return True

			finally:
				self.__perform_deinitialize(bd2)
	#

	#
	# Perform a backup.
	#
	@jk_typing.checkFunctionSignature()
	def performBackup(self,
		backupIdentifier:str,
		backupTasks:typing.List[AbstractThaniyaTask],
		) -> bool:

		self.__checkBackupIdentifierE(backupIdentifier)

		mainLog = jk_logging.ConsoleLogger.create(logMsgFormatter=jk_logging.COLOR_LOG_MESSAGE_FORMATTER)

		with BD2(backupIdentifier, mainLog) as bd2:
			nExpectedBytesToWrite = self.__perform_calcDiskSpaceRequired(bd2, backupTasks)
			assert nExpectedBytesToWrite >= 0

			try:

				self.__perform_initialize(bd2, nExpectedBytesToWrite)
				self.__perform_backup(bd2, backupTasks)
				self.__perform_finalizeBackup(bd2)
				return True

			finally:
				self.__perform_deinitialize(bd2)
	#

#


















