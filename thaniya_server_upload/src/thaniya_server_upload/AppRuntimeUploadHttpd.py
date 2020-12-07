


import os
import typing

import jk_typing
import jk_logging
import jk_simpleobjpersistency
import jk_utils
from jk_appmonitoring import RDirectory, RFileSystem, RFileSystemCollection
import jk_mounting

from thaniya_common import AppRuntimeBase
from thaniya_common.cfg import AbstractAppCfg
from thaniya_server_sudo import SudoScriptRunner

from thaniya_server.utils import SecureRandomDataGenerator
from thaniya_server.utils import SecureRandomIDGenerator
from thaniya_server.utils import Scheduler
from thaniya_server.session import SessionIDGenerator
from thaniya_server.session import MemorySessionManager
from thaniya_server.usermgr import BackupUserManager
from thaniya_server.jobs import JobQueue
from thaniya_server.jobs import JobProcessingEngine
from thaniya_server.api import APIAuthentificator

from .IAppRuntimeUserMgr import IAppRuntimeUserMgr
from .UploadHttpdCfg import UploadHttpdCfg
from .slots import UploadSlotManager
#from .JobProcessor_Noop import JobProcessor_Noop








class AppRuntimeUploadHttpd(AppRuntimeBase, IAppRuntimeUserMgr):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	#
	# @param		jk_logging.AbstractLogger log			A log object for informational and error output
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, mainFilePath:str, log:jk_logging.AbstractLogger):
		super().__init__(mainFilePath, log)

		self.__secureIDGen = SecureRandomIDGenerator()

		self.__secureRNG = SecureRandomDataGenerator()

		self.__sudoScriptRunner = SudoScriptRunner(self.cfg.sudo["scriptsDir"])

		self.__userMgr = BackupUserManager(self.cfg.userMgr["usersDir"], False, log)

		self.__fileSystemCollection = RFileSystemCollection()

		"""
		for mountInfo in jk_mounting.Mounter().getMountInfos2(isRegularDevice=True):
			assert isinstance(mountInfo, jk_mounting.MountInfo)
			try:
				statvfs = os.statvfs(mountInfo.mountPoint)
			except:
				# BUG: if file paths contain spaces the output of 'mount' is not parsed correctly by jk_mounting. current hotfix: skip these file systems.
				continue
			
			if not self.__fileSystemCollection.hasMountPoint(mountInfo.mountPoint):
				self.__fileSystemCollection.registerFileSystem(RFileSystem(mountInfo.mountPoint, mountInfo.mountPoint, mountInfo.device, False))
		"""

		# ----

		"""
		with log.descend("Initializing backup volume manager ...") as log2:
			self.__backupVolumeMgr = BackupVolumeManager(
				staticVolumeCfgDirPath = self.cfg.volumeMgr["staticVolumeCfgDir"],
				stateDirPath = self.cfg.volumeMgr["stateDir"],
				bCreateMissingDirectories = False,
				log = log2,
			)
		"""

		with log.descend("Launching internal scheduler ...") as log2:
			self.__scheduler = Scheduler()
			self.__scheduler.startBackgroundThread()

		#self.__cached_usageInfos = jk_utils.VolatileValue(self.__getUsageInfos, 15)

		self.__apiAuth = APIAuthentificator(self, self.cfg.httpd["apiAuthTimeout"])
		self.__apiSessionIDGen = SessionIDGenerator()
		self.__apiSessionMgr = MemorySessionManager(self.cfg.httpd["apiSessionTimeout"])

		with log.descend("Initializing slot manager ...") as log2:
			_logSlotProcessing = jk_logging.FileLogger.create(
				filePath = self.cfg.slotMgr["logFile"],
				rollOver = self.cfg.slotMgr["logRollover"],
				fileMode = self.ioCtx.chmodValueFileI,
			)
			_logSlotProcessing.info("#" * 160)

			self.__uploadSlotMgr = UploadSlotManager(
				ioContext = self.ioCtx,
				backupUserManager = self.__userMgr,
				sudoScriptRunner = self.__sudoScriptRunner,
				slotStatesDirPath = self.cfg.slotMgr["stateDir"],
				uploadResultDirPath = self.cfg.slotMgr["resultDir"],
				nSecuritySpaceMarginBytes = int(self.cfg.slotMgr["securitySpaceMarginBytes"]),
				log = log2,
			)

			self.__scheduler.scheduleRepeat(
				waitSeconds = 15,
				jobCallable = self.__uploadSlotMgr.checkAndManageSlots,
				jobArguments = [
					_logSlotProcessing
				]
			)

		"""
		with log.descend("Initializing job processing ...") as log2:
			#_logJobProcessing = jk_logging.FileLogger.create(
			#	filePath = self.cfg.jobProcessing["logFile"],
			#	rollOver = self.cfg.jobProcessing["logRollover"],
			#	fileMode = self.ioCtx.chmodValueFileI,
			#)

			#self.__jobProcessingEngine = JobProcessingEngine(
			#	_logJobProcessing,
			#	ioContext = self.ioCtx,
			#	)

			self.__jobQueue = JobQueue(
				ioContext = self.ioCtx,
				dirPath = self.cfg.jobProcessing["jobQueueDir"],
				bResetJobStateOnLoad = True,
				log = log2
				)

			self.__jobProcessingEngine.start(self.__jobQueue)

		with log.descend("Registering job processors ...") as log2:
			#self.__jobProcessingEngine.register(JobProcessor_Noop(), log2)
			#self.__jobProcessingEngine.register(JobProcessor_InsertBackupIntoArchive(), log2)
			pass
		"""

		# --------

		with log.descend("Updating file system collection ...") as log2:
			self.updateFileSystemCollection(log2)

		"""
		with log.descend("Updating archives ...") as log2:
			self.__addArchivesNotYetUsed(log2)
		"""
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	"""
	@property
	def archiveMgr(self) -> ArchiveManager:
		return self.__archiveManager
	#
	"""

	@property
	def secureIDGen(self) -> SecureRandomIDGenerator:
		return self.__secureIDGen
	#

	@property
	def secureRNG(self) -> SecureRandomDataGenerator:
		return self.__secureRNG
	#

	@property
	def userMgr(self) -> BackupUserManager:
		return self.__userMgr
	#

	"""
	@property
	def backupVolumeMgr(self) -> BackupVolumeManager:
		return self.__backupVolumeMgr
	#

	@property
	def fileSystemCollection(self) -> RFileSystemCollection:
		return self.__fileSystemCollection
	#
	"""

	@property
	def apiSessionMgr(self) -> MemorySessionManager:
		return self.__apiSessionMgr
	#

	@property
	def apiAuth(self) -> APIAuthentificator:
		return self.__apiAuth
	#

	@property
	def apiSessionIDGen(self) -> SessionIDGenerator:
		return self.__apiSessionIDGen
	#

	@property
	def uploadSlotMgr(self) -> UploadSlotManager:
		return self.__uploadSlotMgr
	#

	@property
	def fileSystemCollection(self) -> RFileSystemCollection:
		return self.__fileSystemCollection
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _loadConfigurationCallback(self, log:jk_logging.AbstractLogger) -> AbstractAppCfg:
		return UploadHttpdCfg.load()
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def onSIGUSR1(self, *args):
		try:
			with self.log.descend("Signal SIGUSR1 received -> reloading runtime data ...") as log2:
				log2.notice("Reloading users ...")
				self.__userMgr.reloadUsers()
				#log2.notice("Updating backup volume list ...")
				#self.__backupVolumeMgr.update(log2)
				log2.notice("Updating file system collection ...")
				self.updateFileSystemCollection(log2)
				#log2.notice("Updating archives ...")
				#self.__addArchivesNotYetUsed(log2)
				log2.notice("Updating job queue ...")
				self.__jobQueue.update(log2)
		except:
			# swallow all exceptions; they have been logged anyway
			pass
	#

	"""
	def __addArchivesNotYetUsed(self, log:jk_logging.AbstractLogger):
		for bvi in self.__backupVolumeMgr.listVolumes(log):
			if bvi.isValid and bvi.isActive and not self.__archiveManager.hasArchive(bvi.backupVolumeID):
				self.__archiveManager.register(
					volume=bvi,
					bReadWrite=True,			# TODO: in the future we might want to modify this; for now every archive is automatically loaded as read-write
					log=log)
	#
	"""

	def updateFileSystemCollection(self, log:jk_logging.AbstractLogger):
		self.__fileSystemCollection.clear()
		
		rootAppFSPath = jk_utils.fsutils.findMountPoint(self.appBaseDirPath)
		self.__fileSystemCollection.registerFileSystem(RFileSystem(rootAppFSPath, rootAppFSPath, None, False))
		self.__fileSystemCollection.registerDirectory(RDirectory("ThaniyaApp", self.appBaseDirPath, 60*5))

		rootEtcFSPath = jk_utils.fsutils.findMountPoint("/etc")
		if not self.__fileSystemCollection.hasMountPoint(rootEtcFSPath):
			self.__fileSystemCollection.registerFileSystem(RFileSystem(rootEtcFSPath, rootEtcFSPath, None, False))
		self.__fileSystemCollection.registerDirectory(RDirectory("ThaniyaCfg", "/etc/thaniya", 60*5))

		if not self.__fileSystemCollection.hasMountPoint(self.__uploadSlotMgr.fsMountPoint):
			self.__fileSystemCollection.registerFileSystem(RFileSystem("ThaniyaSlots", self.__uploadSlotMgr.fsMountPoint, None, False))
	#

#

















