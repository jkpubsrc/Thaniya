


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
from thaniya_common.utils import IOContext
from thaniya_server.utils import SecureRandomDataGenerator
from thaniya_server.utils import SecureRandomIDGenerator
from thaniya_server.utils import Scheduler
from thaniya_server.session import SessionIDGenerator
from thaniya_server.session import MemorySessionManager
from thaniya_server.usermgr import BackupUserManager
from thaniya_server_sudo import SudoScriptRunner
from thaniya_server_archive.volumes import BackupVolumeManager
from thaniya_server_archive.ArchiveHttpdCfg import ArchiveHttpdCfg
from thaniya_server_upload.UploadHttpdCfg import UploadHttpdCfg
from thaniya_server.utils.ProcessFilter import ProcessFilter
from thaniya_server.utils.ProcessNotifier import ProcessNotifier
from thaniya_server_upload.slots import UploadSlotManager










class AppRuntimeServerCtrl(object):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	#
	# @param		jk_logging.AbstractLogger log			A log object for informational and error output
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, mainFilePath:str, log:jk_logging.AbstractLogger):
		mainFilePath = os.path.abspath(mainFilePath)
		self.__appBaseDirPath = os.path.dirname(mainFilePath)
		self.__ioCtx = IOContext()
		self.__log = log

		self.__uploadHttpCfg = UploadHttpdCfg.load()
		self.__archiveHttpCfg = ArchiveHttpdCfg.load()

		self.__secureIDGen = SecureRandomIDGenerator()

		self.__secureRNG = SecureRandomDataGenerator()

		self.__sudoScriptRunner = SudoScriptRunner(self.__archiveHttpCfg.sudo["scriptsDir"])

		self.__userMgr = BackupUserManager(self.__archiveHttpCfg.userMgr["usersDir"], True, log)

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

		with log.descend("Initializing slot manager ...") as log2:
			self.__uploadSlotMgr = UploadSlotManager(
				ioContext = self.ioCtx,
				backupUserManager = self.__userMgr,
				sudoScriptRunner = self.__sudoScriptRunner,
				slotStatesDirPath = self.__uploadHttpCfg.slotMgr["stateDir"],
				uploadResultDirPath = self.__uploadHttpCfg.slotMgr["resultDir"],
				nSecuritySpaceMarginBytes = int(self.__uploadHttpCfg.slotMgr["securitySpaceMarginBytes"]),
				log = log2,
			)

		with log.descend("Initializing bolume manager ...") as log2:
			self.__backupVolumeMgr = BackupVolumeManager(
				staticVolumeCfgDirPath = self.__archiveHttpCfg.volumeMgr["staticVolumeCfgDir"],
				stateDirPath = self.__archiveHttpCfg.volumeMgr["stateDir"],
				log = log2,
				bCreateMissingDirectories = False,
		)

		"""
		self.__scheduler = Scheduler()
		#self.__scheduler.scheduleRepeat(15, self.uploadSlotMgr.cleanup, [ log ])
		self.__scheduler.startBackgroundThread()

		#self.__cached_usageInfos = jk_utils.VolatileValue(self.__getUsageInfos, 15)
		"""

		self.__processFilter_thaniyaArchiveHttpd = ProcessFilter(cmdMatcher= lambda x: x.find("python") > 0, argsMatcher= lambda x: x and (x.find("thaniya-archive-httpd.py") >= 0))
		self.__processFilter_thaniyaSFTPSessions = ProcessFilter(userNameMatcher= lambda x: (x == "thaniya") and x.startswith("thaniya_"))
		self.__processNotifier = ProcessNotifier(self.__processFilter_thaniyaArchiveHttpd)

		# register file systems
		self.updateFileSystemCollection()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def uploadSlotMgr(self) -> str:
		return self.__uploadSlotMgr
	#

	@property
	def processFilter_thaniyaSFTPSessions(self) -> ProcessFilter:
		return self.__processFilter_thaniyaSFTPSessions
	#

	@property
	def processFilter_thaniyaArchiveHttpd(self) -> ProcessFilter:
		return self.__processFilter_thaniyaArchiveHttpd
	#

	@property
	def processFilter_thaniyaArchiveHttpd(self) -> ProcessFilter:
		return self.__processFilter_thaniyaArchiveHttpd
	#

	@property
	def ioCtx(self) -> IOContext:
		return self.__ioCtx
	#

	@property
	def appBaseDirPath(self) -> str:
		return self.__appBaseDirPath
	#

	@property
	def archiveHttpCfg(self) -> AbstractAppCfg:
		return self.__archiveHttpCfg
	#

	@property
	def log(self) -> jk_logging.AbstractLogger:
		return self.__log
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

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _loadConfigurationCallback(self, log:jk_logging.AbstractLogger) -> AbstractAppCfg:
		return ArchiveHttpdCfg.load()
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def updateFileSystemCollection(self):
		self.__fileSystemCollection.clear()
		
		rootAppFSPath = jk_utils.fsutils.findMountPoint(self.appBaseDirPath)
		self.__fileSystemCollection.registerFileSystem(RFileSystem(rootAppFSPath, rootAppFSPath, None, False))
		self.__fileSystemCollection.registerDirectory(RDirectory("ThaniyaApp", self.appBaseDirPath, 60*5))

		rootEtcFSPath = jk_utils.fsutils.findMountPoint("/etc")
		if not self.__fileSystemCollection.hasMountPoint(rootEtcFSPath):
			self.__fileSystemCollection.registerFileSystem(RFileSystem(rootEtcFSPath, rootEtcFSPath, None, False))
		self.__fileSystemCollection.registerDirectory(RDirectory("ThaniyaCfg", "/etc/thaniya", 60*5))

		for bvi in self.__backupVolumeMgr.listVolumes(self.log):
			if bvi.isActive:
				if not self.__fileSystemCollection.hasMountPoint(bvi.device.mountPoint):
					self.__fileSystemCollection.registerFileSystem(RFileSystem(bvi.device.mountPoint, bvi.device.mountPoint, bvi.device.devPath, False))
				self.__fileSystemCollection.registerDirectory(RDirectory("VOL:" + bvi.backupVolumeID.hexData, bvi.backupBaseDirPath, 60))
	#

	def notifyOtherThaniyaProcesses(self) -> int:
		return self.__processNotifier.notifySIGUSR1()
	#

#



















