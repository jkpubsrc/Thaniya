

import typing
import re
import time
import os
import random
import datetime

import jk_typing
import jk_logging
import jk_utils
import jk_prettyprintobj

from thaniya_common.utils import IOContext
#from thaniya_server.utils import IDiskUsageProvider

from ..volumes.BackupVolumeInfo import BackupVolumeInfo

from .Backup import Backup









#
# This class implements everything to manage backups. It is NOT responsible for creating individual backups, it just manages these backups.
# This class is not ment to be used as a standalone class. However it is implemented in a way that it can be tested as a standalone class.
#
class ArchiveDataStoreBase(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	#
	# Constructor Method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, ioContext:IOContext, dataDirPath:str, tempDirPath:str, bReadWrite:bool, log:jk_logging.AbstractLogger):
		self._ioContext = ioContext

		dataDirPath = os.path.normpath(dataDirPath)
		assert os.path.isdir(dataDirPath)
		self.__dataDirPath = os.path.abspath(dataDirPath)
		mountPointDataDirPath = jk_utils.fsutils.findMountPoint(dataDirPath)
		if bReadWrite:
			ioContext.setDirMode(self.__dataDirPath)

		tempDirPath = os.path.normpath(tempDirPath)
		assert os.path.isdir(tempDirPath)
		self.__tempDirPath = os.path.abspath(tempDirPath)
		mountPointTempDirPath = jk_utils.fsutils.findMountPoint(tempDirPath)
		if bReadWrite:
			ioContext.setDirMode(self.__tempDirPath)

		if mountPointDataDirPath != mountPointTempDirPath:
			raise Exception("Data directory and temporary directory do not reside on the same file system!")

		self.__fileSystemBlockSize = os.statvfs(mountPointDataDirPath).f_bsize

		# TODO: Centralize this getFolderSize() functionality in the future. For now we stick with this simple approach of implementing it here.
		#self.__mountInfo = jk_mounting.Mounter().getMountInfoByMountPoint(mountPointDataDirPath, raiseException=True)

		self.__bReadWrite = bReadWrite						# bool
		self.__log = log									# jk_logging.AbstractLogger

		self.__backups = None								# Backup[]
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def fsBlockSize(self) -> int:
		return self.__fileSystemBlockSize
	#

	@property
	def isReadWrite(self) -> bool:
		return self.__bReadWrite
	#

	@property
	def isReadOnly(self) -> bool:
		return not self.__bReadWrite
	#

	@property
	def dataDirPath(self) -> str:
		return self.__dataDirPath
	#

	@property
	def tempDirPath(self) -> str:
		return self.__tempDirPath
	#

	@property
	def backups(self) -> list:
		if self.__backups is None:
			self.__backups = self.__scanForBackups()
		return self.__backups
	#

	# TODO: Centralize this functionality in the future. For now we stick with this simple approach of implementing it here.
	#@property
	#def mountInfo(self) -> jk_mounting.MountInfo:
	#	return self.__mountInfo
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"isReadWrite",
			"dataDirPath",
			"tempDirPath",
		]
	#

	def __scanForBackups(self) -> typing.List[Backup]:
		backups = []
		with self.__log.descend("Scanning for backups ...") as log2:
			log2.notice("Archive base directory: " + self.__dataDirPath)
			for fe in os.scandir(self.__dataDirPath):
				if fe.is_dir():
					jData = Backup.tryParseDirName(fe.name)
					lBackupStartDateTime = ( jData["year"], jData["month"], jData["day"], jData["hour"], jData["minute"], jData["second"] )
					backup = Backup(fe.path)
					if (backup.systemName == jData["systemName"]) and (backup.backupUserName == jData["userName"]) \
						and (backup.lBackupStartDateTime == lBackupStartDateTime) \
						and (backup.backupIdentifier == jData["backupIdentifier"]):
						# everything is okay
						pass
					else:
						# file name is wrong
						log2.warning("Data in directory name does not match data from info file!")
						log2.warning("Displaying data parsed from file name vs. data from backup container:")
						log2.warning("\tsystemName: " + repr(jData["systemName"]) + " vs. " + repr(backup.systemName))
						log2.warning("\tuserName: " + repr(jData["userName"]) + " vs. " + repr(backup.backupUserName))
						log2.warning("\tlBackupStartDateTime: " + repr(lBackupStartDateTime) + " vs. " + repr(backup.lBackupStartDateTime))
						log2.warning("\tbackupIdentifier: " + repr(jData["backupIdentifier"]) + " vs. " + repr(backup.backupIdentifier))
					backups.append(backup)
				else:
					log2.notice("Ignoring file: " + fe.name)
		return backups
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	"""
	# TODO: Centralize this functionality in the future. For now we stick with this simple approach of implementing it here.
	def getUsageInfos(self) -> typing.List[DiskUsageValue]:
		return [
			DiskUsageValue(
				self.__mountInfo,
				"Archive " + self.name,
				"data",
				jk_utils.AmountOfBytes(jk_utils.fsutils.getFolderSize(self.__dataDirPath)),
			),
			DiskUsageValue(
				"Archive " + self.name,
				"temp",
				jk_utils.AmountOfBytes(jk_utils.fsutils.getFolderSize(self.__tempDirPath)),
			),
		]
	#
	"""

	#
	# Something has been modified externally. Clean the internal cach(es).
	#
	def invalidate(self):
		self.__backups = None
	#

	"""
	This method has been replaced by moving that logic into a facade: class BackupManager

	def getBackups(self, systemName:str = None, userName:str = None, backupIdentifier:str = None, year:int = None, month:int = None, day:int = None) -> list:
		if self.__backups is None:
			self.__backups = self.__scanForBackups()
	#
	"""

	#
	# Generate a temporary directory path (but do not create the directory!)
	#
	@jk_typing.checkFunctionSignature()
	def _generateTempDirPath(self, dt:datetime.datetime, systemName:str, backupUserName:str, backupIdentifier:str) -> str:
		dirName = Backup.buildRecommendedDirName(dt=dt, systemName=systemName, backupUserName=backupUserName, backupIdentifier=backupIdentifier)
		return os.path.join(self.__tempDirPath, dirName)
	#

	@jk_typing.checkFunctionSignature()
	def _generateDataDirPath(self, dt:datetime.datetime, systemName:str, backupUserName:str, backupIdentifier:str) -> str:
		dirName = Backup.buildRecommendedDirName(dt=dt, systemName=systemName, backupUserName=backupUserName, backupIdentifier=backupIdentifier)
		return os.path.join(self.__dataDirPath, dirName)
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#















