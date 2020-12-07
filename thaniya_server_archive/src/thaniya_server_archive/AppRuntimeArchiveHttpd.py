


import os
import typing

import jk_typing
import jk_logging
import jk_utils
from jk_appmonitoring import RDirectory, RFileSystem, RFileSystemCollection

from thaniya_common import AppRuntimeBase
from thaniya_common.cfg import AbstractAppCfg

from thaniya_server.utils import SecureRandomDataGenerator
from thaniya_server.utils import SecureRandomIDGenerator
from thaniya_server.utils import Scheduler
from thaniya_server.session import SessionIDGenerator
from thaniya_server.session import MemorySessionManager
from thaniya_server.usermgr import BackupUserManager
#from thaniya_server import IAppRuntimeUserMgr
#from thaniya_server_sudo import SudoScriptRunner
from thaniya_server.jobs import JobQueue
from thaniya_server.jobs import JobProcessingEngine

from .ArchiveHttpdCfg import ArchiveHttpdCfg
from .volumes import BackupVolumeManager
from .archive import ArchiveDataStore
from .archive import ArchiveManager
from .JobProcessor_InsertBackupIntoArchive import JobProcessor_InsertBackupIntoArchive
from .JobProcessor_Noop import JobProcessor_Noop
from .archive.FileNamePattern import FileNamePattern
from .archive.ProcessingRule import ProcessingRule
from .archive.ProcessingRuleSet import ProcessingRuleSet
from .IncomingUploadMonitor import IncomingUploadMonitor
from .BackupManager import BackupManager









class AppRuntimeArchiveHttpd(AppRuntimeBase):		#, IAppRuntimeUserMgr):

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

		#self.__sudoScriptRunner = SudoScriptRunner(self.cfg.sudo["scriptsDir"])

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

		with log.descend("Initializing backup volume manager ...") as log2:
			self.__backupVolumeMgr = BackupVolumeManager(
				staticVolumeCfgDirPath = self.cfg.volumeMgr["staticVolumeCfgDir"],
				stateDirPath = self.cfg.volumeMgr["stateDir"],
				bCreateMissingDirectories = False,
				log = log2,
			)

		with log.descend("Initializing archive manager ...") as log2:
			self.__archiveManager = ArchiveManager()

		"""
		#self.__cached_usageInfos = jk_utils.VolatileValue(self.__getUsageInfos, 15)
		"""

		with log.descend("Initializing job processing ...") as log2:
			_logJobProcessing = jk_logging.FileLogger.create(
				filePath=self.cfg.jobProcessing["logFile"],
				rollOver=self.cfg.jobProcessing["logRollover"],
				fileMode=self.ioCtx.chmodValueFileI,
				)
			_logJobProcessing.info("#" * 160)

			processingRuleSet = ProcessingRuleSet([
				ProcessingRule(FileNamePattern("*.tar"), "gzip"),
			])

			self.__jobProcessingEngine = JobProcessingEngine(
				_logJobProcessing,
				ioContext = self.ioCtx,
				processingRuleSet = processingRuleSet,
				archiveMgr = self.__archiveManager,
				)

			self.__jobQueue = JobQueue(
				ioContext=self.ioCtx,
				dirPath=self.cfg.jobProcessing["jobQueueDir"],
				bResetJobStateOnLoad=True,
				log=log2
				)

			self.__jobProcessingEngine.start(self.__jobQueue)

		with log.descend("Registering job processors ...") as log2:
			self.__jobProcessingEngine.register(JobProcessor_Noop(), log2)
			self.__jobProcessingEngine.register(JobProcessor_InsertBackupIntoArchive(), log2)

		with log.descend("Creating scheduler ...") as log2:
			self.__scheduler = Scheduler()
			self.__scheduler.startBackgroundThread()

		with log.descend("Setting up incoming upload monitor ...") as log2:
			self.__incomingMonitor = IncomingUploadMonitor(self.cfg.jobProcessing["incomingBackupsDir"], self.__jobQueue)
			self.__scheduler.scheduleRepeat(15, self.__incomingMonitor.checkForIncoming, [ log ])

		# facades

		self.__backupManager = BackupManager(self)

		# --------

		with log.descend("Updating archives ...") as log2:
			self.__addArchivesNotYetUsed(log2)

		with log.descend("Updating file system collection ...") as log2:
			self.updateFileSystemCollection(log2)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def jobQueue(self) -> JobQueue:
		return self.__jobQueue
	#

	@property
	def archiveMgr(self) -> ArchiveManager:
		return self.__archiveManager
	#

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

	@property
	def backupVolumeMgr(self) -> BackupVolumeManager:
		return self.__backupVolumeMgr
	#

	@property
	def fileSystemCollection(self) -> RFileSystemCollection:
		return self.__fileSystemCollection
	#

	#
	# Returns a facade that provides access to backups
	#
	@property
	def backupMgr(self) -> BackupManager:
		return self.__backupManager
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _loadConfigurationCallback(self, log:jk_logging.AbstractLogger) -> AbstractAppCfg:
		return ArchiveHttpdCfg.load()
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def onSIGUSR1(self, *args):
		try:
			with self.log.descend("Signal SIGUSR1 received -> reloading runtime data ...") as log2:
				log2.notice("Reloading users ...")
				self.__userMgr.reloadUsers()
				log2.notice("Updating backup volume list ...")
				self.__backupVolumeMgr.update(log2)
				log2.notice("Updating file system collection ...")
				self.updateFileSystemCollection(log2)
				log2.notice("Updating archives ...")
				self.__addArchivesNotYetUsed(log2)
				log2.notice("Updating job queue ...")
				self.__jobQueue.update(log2)
		except:
			# swallow all exceptions; they have been logged anyway
			pass
	#

	def __addArchivesNotYetUsed(self, log:jk_logging.AbstractLogger):
		for bvi in self.__backupVolumeMgr.listVolumes(log):
			if bvi.isValid and bvi.isActive and not self.__archiveManager.hasArchive(bvi.backupVolumeID):
				self.__archiveManager.register(
					volume=bvi,
					bReadWrite=True,			# TODO: in the future we might want to modify this; for now every archive is automatically loaded as read-write
					log=log)
	#

	def updateFileSystemCollection(self, log:jk_logging.AbstractLogger):
		self.__fileSystemCollection.clear()
		
		rootAppFSPath = jk_utils.fsutils.findMountPoint(self.appBaseDirPath)
		self.__fileSystemCollection.registerFileSystem(RFileSystem(rootAppFSPath, rootAppFSPath, None, False))
		self.__fileSystemCollection.registerDirectory(RDirectory("ThaniyaApp", self.appBaseDirPath, 60*5))

		rootEtcFSPath = jk_utils.fsutils.findMountPoint("/etc")
		if not self.__fileSystemCollection.hasMountPoint(rootEtcFSPath):
			self.__fileSystemCollection.registerFileSystem(RFileSystem(rootEtcFSPath, rootEtcFSPath, None, False))
		self.__fileSystemCollection.registerDirectory(RDirectory("ThaniyaCfg", "/etc/thaniya", 60*5))

		for a in self.__archiveManager.archives:
			if not self.__fileSystemCollection.hasMountPoint(a.mountPoint):
				self.__fileSystemCollection.registerFileSystem(RFileSystem(a.mountPoint, a.mountPoint, a.devPath, False))
			self.__fileSystemCollection.registerDirectory(RDirectory("Arch:" + a.backupVolumeID.hexData, a.archiveDirPath, 60))

		"""
		for bvi in self.__backupVolumeMgr.listVolumes(log):
			if bvi.isActive:
				if not self.__fileSystemCollection.hasMountPoint(bvi.device.mountPoint):
					self.__fileSystemCollection.registerFileSystem(RFileSystem(bvi.device.mountPoint, bvi.device.mountPoint, bvi.device.devPath, False))
				self.__fileSystemCollection.registerDirectory(RDirectory("VOL:" + bvi.backupVolumeID.hexData, bvi.backupBaseDirPath, 60))
		"""
	#

#

















