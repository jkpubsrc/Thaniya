



import os
import typing
import time

import jk_typing
import jk_utils
import jk_logging
import jk_json
import jk_prettyprintobj
import jk_packunpack

from thaniya_common.utils import IOContext

from thaniya_server.jobs import Job
from thaniya_server.jobs import AbstractJobProcessor
from thaniya_server.jobs import JobProcessingCtx

from .archive import ArchivedBackupInfoFile
from .archive import ArchiveManager
from .archive import ArchiveDataStore
from .archive.ProcessingRule import ProcessingRule
from .archive.ProcessingRuleSet import ProcessingRuleSet




#
# Some methods in the job processor follow the convention that all data required is provided by an instance of <c>_JobProcessingContext</c> directly.
# So there is no need for almost no method to access the raw job data directly. (However it *is* necessary to write state data to the job directly.)
# The reason for this convention is to simplify development and avoid implementation errors as this class is quite complex.
#
class _JobProcessingContext(object):

	def __init__(self, job:Job):
		self.archive = None					# ArchiveDataStore		The archive selected that will receive the backup data.
		self.__job = job					# Job					The job that is to be processed
		self.nFSBlockSize = -1				# int					The bock size of the target file system we are going to write to.
		self.processingRuleSet = None					# ProcessingRuleSet		The rules we might want to use.
		self.fromDirPath = None				# str					The source directory from which files will be copied.
		self.toTempDirPath = None			# str					The temporary target directory within the archive to which files will be copied to.
		self.terminationFlag = None			# TerminationFlag		A termination flag to be able to interrupt the job (e.g. to shut down the application immediately).
		self.dataFileNames = None			# str[]					The names of regular files to upload
		self.metaFileNames = None			# str[]					The names of meta files to upload
		# prepare job processing state: this is probably the very first time we run the job;

		for key in [ "nTotalBytesUploaded", "nTotalBytesArchived" ]:
			if key not in job.processingStateData:
				job.processingStateData[key] = jk_utils.AmountOfBytes(0)

		for key in [ "filesProcessed", "newDataFileNames", "newMetaFileNames" ]:
			if key not in job.processingStateData:
				job.processingStateData[key] = []
	#

	# TODO: maybe add a prefix so that everyone knows this is a job state?
	@property
	def targetArchiveID(self) -> typing.Union[str,None]:
		return self.__job.processingStateData.get("targetArchiveID")
	#

	# TODO: maybe add a prefix so that everyone knows this is a job state?
	@targetArchiveID.setter
	def targetArchiveID(self, value:str):
		assert isinstance(value, str)
		assert value
		self.__job.processingStateData["targetArchiveID"] = value
	#

	# TODO: maybe add a prefix so that everyone knows this is a job state?
	@property
	def nTotalBytesUploaded(self) -> jk_utils.AmountOfBytes:
		return self.__job.processingStateData["nTotalBytesUploaded"]
	#

	# TODO: maybe add a prefix so that everyone knows this is a job state?
	@nTotalBytesUploaded.setter
	def nTotalBytesUploaded(self, value:jk_utils.AmountOfBytes):
		assert isinstance(value, jk_utils.AmountOfBytes)
		assert value >= 0
		self.__job.processingStateData["nTotalBytesUploaded"] = value
	#

	# TODO: maybe add a prefix so that everyone knows this is a job state?
	@property
	def nTotalBytesArchived(self) -> jk_utils.AmountOfBytes:
		return self.__job.processingStateData["nTotalBytesArchived"]
	#

	# TODO: maybe add a prefix so that everyone knows this is a job state?
	@nTotalBytesArchived.setter
	def nTotalBytesArchived(self, value:jk_utils.AmountOfBytes):
		assert isinstance(value, jk_utils.AmountOfBytes)
		assert value >= 0
		self.__job.processingStateData["nTotalBytesArchived"] = value
	#

	# TODO: maybe add a prefix so that everyone knows this is a job state?
	@property
	def filesProcessed(self) -> list:
		return self.__job.processingStateData["filesProcessed"]
	#

	# TODO: maybe add a prefix so that everyone knows this is a job state?
	@property
	def newDataFileNames(self) -> list:
		return self.__job.processingStateData["newDataFileNames"]
	#

	# TODO: maybe add a prefix so that everyone knows this is a job state?
	@property
	def newMetaFileNames(self) -> list:
		return self.__job.processingStateData["newMetaFileNames"]
	#

	# TODO: maybe find a better name?
	def storeProcessingState(self):
		self.__job.storeProcessingState()
	#

#





class JobProcessor_InsertBackupIntoArchive(AbstractJobProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self):
		super().__init__("InsertBackupIntoArchive")
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Low Level Methods
	################################################################################################################################

	#
	# Copy the specified file to the target directory. If a processing rule is specified the data is processed during copying.
	#
	# @param		str srcFilePath						(required) The file to copy.
	# @param		str destDirPath						(required) The destination directory to write to. This typcially is the target backup directory.
	#													Exactly this makes this method indempotent: The worst case scenario is that a file is copied (and packed)
	#													twice. But as the target file name is always the same, this doesn't matter.
	# @param		ProcessingRule rule					(optional) A processing rule to apply to this file.
	# @param		TerminationFlag terminationFlag		(required) A termination flag that can be used to interrupt processing
	# @param		int fsBlockSize						(required) The file system block size. The number of bytes returned are aligned to this value.
	# @param		AbstractLogger log					(required) A logger that can receive debugging output
	#
	# @return		str destDirPath				The target directory as specified by the caller
	# @return		str destFileName			The destination file name. This is the name the file has finally been renamed to after processing.
	#											This file name might differ from the one specified with <c>srcFilePath</c>.
	# @return		int nFromSize				The size of the resulting file in bytes after copying. (This value is aligned to the value of <c>fsBlockSize</c>.)
	# @return		int nToSize					The size of the resulting file in bytes after copying. (This value is aligned to the value of <c>fsBlockSize</c>.)
	#
	@jk_typing.checkFunctionSignature()
	def ____doCopyProcess(self,
			ioCtx:IOContext,
			srcFilePath:str,
			destDirPath:str,
			rule:typing.Union[ProcessingRule,None],
			terminationFlag:jk_utils.TerminationFlag,
			fsBlockSize:int,
			log:jk_logging.AbstractLogger
		) -> tuple:

		srcDirPath, srcFileName = os.path.split(srcFilePath)
		assert srcDirPath
		assert srcFileName
		assert os.path.isfile(srcFilePath)
		assert fsBlockSize > 0

		destTempFileName = "thaniya$$$tmp$$$.tmp"
		destTempFilePath = os.path.join(destDirPath, destTempFileName)

		if rule is None:
			result = jk_packunpack.Spooler.spoolFile(
				fromFilePath=srcFilePath,
				toFilePath=destTempFilePath,
				bDeleteOriginal=False,
				chModValue=ioCtx.chmodValueFileI,
				terminationFlag=terminationFlag,
				log=log
			)
			destFileName = srcFileName

		else:
			assert isinstance(rule, ProcessingRule)

			result = jk_packunpack.Packer.compressFile2(
				filePath=srcFilePath,
				toFilePath=destTempFilePath,
				compression=rule.compressionAction,
				bDeleteOriginal=False,
				chModValue=ioCtx.chmodValueFileI,
				terminationFlag=terminationFlag,
				log=log
			)
			assert result.compressionFileExt.startswith(".")
			destFileName = srcFileName + result.compressionFileExt

		destFilePath = os.path.join(destDirPath, destFileName)

		# now rename the target file to the correct file name
		if os.path.isfile(destFilePath):
			os.unlink(destFilePath)
		os.rename(destTempFilePath, destFilePath)

		# return result
		nFromSize = result.fromFileSize
		assert nFromSize >= 0
		nFromBlocks = ((nFromSize + fsBlockSize - 1) // fsBlockSize)
		nFromSize = nFromBlocks * fsBlockSize

		nToSize = result.toFileSize
		assert nToSize >= 0
		nToBlocks = ((nToSize + fsBlockSize - 1) // fsBlockSize)
		nToSize = nToBlocks * fsBlockSize

		return destDirPath, destFileName, nFromSize, nToSize
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	#
	# This method copies a single file to the temporary backup target directory (not the final target directory!). Processing is applied
	# based on the configured rules iff <c>bIsMetaFile</c> is <c>False</c>.
	# The job runtime state data is updated accordingly if this method succeeded.
	#
	# This method follows the convention that all data required is provided by an instance of <c>_JobProcessingContext</c> directly.
	# So there is no need for this method (or any other function invoked) to access the raw job data directly.
	# (However it *is* necessary to write state data to the job directly.)
	# The reason for this convention is to simplify development and avoid implementation errors as this class is quite complex.
	#
	# @param		str sourceFileName					(required) The source file to process
	#
	@jk_logging.logDescend("Copying file: {sourceFileName} ...", bWithFinalSuccessMsg=False)
	def _copySingleFileToTargetTempDir(self, pctx:_JobProcessingContext, sourceFileName:str, bIsMetaFile:bool, log:jk_logging.AbstractLogger):
		# check if the file has already been processed

		if sourceFileName in pctx.newMetaFileNames:
			log.notice("Skipping file because it has already been processed: " + sourceFileName)
			return

		# build source file path and check it

		_srcPath = os.path.join(pctx.fromDirPath, sourceFileName)
		if not os.path.isfile(_srcPath):
			raise Exception("Source directory does not contain such a file: " + sourceFileName)

		# find rule to use

		rule = None
		if not bIsMetaFile:
			assert sourceFileName[0] != "_"
			# try to find a rule that applies and copy the data
			rule = pctx.processingRuleSet.tryMatch(sourceFileName)

		# perform the transfer

		#log.notice("Now copying file '{}' ...".format(sourceFileName))
		# TODO: the packer/spooler writes a long log message as INFO; can we replace that by the line above?
		_destTempPath, _newDestFileName, nFromSizeAligned, nToSizeAligned = self.____doCopyProcess(
			pctx.ioContext, _srcPath, pctx.toTempDirPath, rule, pctx.terminationFlag, pctx.nFSBlockSize, log)

		# update current processing state

		pctx.nTotalBytesUploaded += nFromSizeAligned
		pctx.nTotalBytesArchived += nToSizeAligned
		pctx.filesProcessed.append(sourceFileName)
		if bIsMetaFile:
			pctx.newMetaFileNames.append(_newDestFileName)
		else:
			pctx.newDataFileNames.append(_newDestFileName)

		pctx.storeProcessingState()
	#

	#
	# This method copies all job files to the temporary backup target directory (not the final target directory!). Processing is applied
	# based on the configured rules to non-metadata files.
	#
	# This method follows the convention that all data required is provided by an instance of <c>_JobProcessingContext</c> directly.
	# So there is no need for this method (or any other function invoked) to access the raw job data directly.
	# (However it *is* necessary to write state data to the job directly.)
	# The reason for this convention is to simplify development and avoid implementation errors as this class is quite complex.
	#
	def _copyAllFilesToTargetTempDir(self, pctx:_JobProcessingContext, log:jk_logging.AbstractLogger):
		for sourceFileName in pctx.dataFileNames:
			self._copySingleFileToTargetTempDir(pctx, sourceFileName, False, log)
		for sourceFileName in pctx.metaFileNames:
			self._copySingleFileToTargetTempDir(pctx, sourceFileName, True, log)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# This method expects the following extra keys present in <c>ctx</c>:
	#
	# * <c>IOContext ioContext</c> : The IO context
	# * <c>ArchiveManager archiveMgr</c> : The archive manager
	# * <c>ProcessingRuleSet processingRuleSet</c> : The processing rule set to apply to uploads
	#
	@jk_typing.checkFunctionSignature()
	def processJob(self, ctx:JobProcessingCtx, job:Job):
		# initialize a _JobProcessingContext data structure
		pctx = _JobProcessingContext(job)
		pctx.processingRuleSet = ctx.processingRuleSet
		pctx.ioContext = ctx.ioContext
		pctx.terminationFlag = ctx.terminationFlag

		pctx.fromDirPath = job.jobData["dirPath"]
		pctx.dataFileNames = job.jobData["dataFileNames"]
		pctx.metaFileNames = job.jobData["metaFileNames"]

		tBackupStart = jk_utils.TimeStamp(job.jobData["tBackupStart"])
		tBackupEnd = jk_utils.TimeStamp(job.jobData["tBackupEnd"])
		dClientBackupDuration = job.jobData["dClientBackupDuration"]
		nSize = job.jobData["sizeInBytes"]
		systemName = job.jobData["systemName"]
		backupUserName = job.jobData["backupUserName"]
		backupIdentifier = job.jobData["backupIdentifier"]

		# get an archive and a temporary archive upload directory

		with ctx.log.descend("Selecting archive to store the data in ...") as log2:
			_archive, _tempDirPath = ctx.archiveMgr.getArchiveForIncomingBackup(
				dt=tBackupStart.dateTime,
				systemName=systemName,
				backupUserName=backupUserName,
				backupIdentifier=backupIdentifier,
				nMaxSizeOfBackup=int(nSize),
				archiveID=pctx.targetArchiveID
			)
			assert _archive
			# TODO: handle the case if no suitable archive is found!

			pctx.archive = _archive
			pctx.nFSBlockSize = _archive.fsBlockSize
			pctx.toTempDirPath = _tempDirPath
			pctx.targetArchiveID = _archive.identifier.hexData
			pctx.storeProcessingState()

		# upload all data to the temporary directory

		with ctx.log.descend("Copying data into the archive ...") as log2:
			self._copyAllFilesToTargetTempDir(pctx, log2)

		# now accept the backup

		with ctx.log.descend("Registering the backup in the archive ...") as log2:
			# create a backup information file

			bif = ArchivedBackupInfoFile()
			bif.setValue("tBackupStart", tBackupStart)
			bif.setValue("tBackupEnd", tBackupEnd)
			bif.setValue("nTotalBytesUploaded", pctx.nTotalBytesUploaded)
			bif.setValue("nTotalBytesArchived", pctx.nTotalBytesArchived)
			bif.setValue("dClientBackupDuration", dClientBackupDuration)
			bif.setValue("systemName", systemName)
			bif.setValue("backupUserName", backupUserName)
			bif.setValue("backupIdentifier", backupIdentifier)

			# store the data in the archive
			pctx.archive.acceptIncomingBackup(
				tempDirPath=pctx.toTempDirPath,
				backupInfoFile=bif,
				dataFileNames=pctx.newDataFileNames,
				metaFileNames=pctx.newMetaFileNames,
				log=log2,
			)

		# delete all files that have been moved into the backup

		with ctx.log.descend("As all data now has been processed, removing temporary upload directory ...") as log2:
			ctx.ioContext.removeDir(pctx.fromDirPath)
	#

#























