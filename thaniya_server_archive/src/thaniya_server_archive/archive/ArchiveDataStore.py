

import typing
import re
import time
import os
import random
import datetime

import jk_typing
import jk_logging
import jk_prettyprintobj

from thaniya_common.utils import IOContext
from thaniya_server.utils import LockFile
from thaniya_server.utils import InUseFlag

from ..volumes.BackupVolumeInfo import BackupVolumeInfo
from ..volumes.BackupVolumeID import BackupVolumeID
from .ArchiveDataStoreBase import ArchiveDataStoreBase
from .ArchivedBackupInfoFile import ArchivedBackupInfoFile
from .Backup import Backup









class ArchiveDataStore(ArchiveDataStoreBase):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	#
	# Constructor Method.
	#
	# @param			obj identifier			An identifier that uniquely identifies this archive.
	#											This identifier should be identical to the backup volume that hosts this archive.
	#											This identifier is the connection between both concepts.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, ioContext:IOContext, volume:BackupVolumeInfo, bReadWrite:bool, log:jk_logging.AbstractLogger):
		archiveDirPath = os.path.join(volume.backupBaseDirPath, "THANIYA-ARCHIVE")
		ioContext.ensureDirExists(archiveDirPath)
		ioContext.setDirMode(archiveDirPath)

		dataDirPath = os.path.join(archiveDirPath, "data")
		log.notice("Using for archive data: " + dataDirPath)
		ioContext.ensureDirExists(dataDirPath)

		tempDirPath = os.path.join(archiveDirPath, "temp")
		log.notice("Using for temporary data: " + tempDirPath)
		ioContext.ensureDirExists(tempDirPath)

		super().__init__(ioContext, dataDirPath, tempDirPath, bReadWrite, log)

		if bReadWrite:
			lockFilePath = os.path.join(archiveDirPath, "using.lock")
			log.notice("Lock file: " + lockFilePath)
			self.__lockFile = LockFile(lockFilePath)
		else:
			self.__lockFile = False

		self.__volume = volume
		self.__archiveDirPath = archiveDirPath
		self.__inUseFlag = InUseFlag(self.__volume.backupVolumeID.hexData)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def inUseFlag(self) -> InUseFlag:
		return self.__inUseFlag
	#

	@property
	def volume(self) -> BackupVolumeInfo:
		return self.__volume
	#

	@property
	def identifier(self) -> BackupVolumeID:
		return self.__volume.backupVolumeID
	#

	@property
	def backupVolumeID(self) -> BackupVolumeID:
		return self.__volume.backupVolumeID
	#

	@property
	def mountPoint(self) -> str:
		return self.__volume.device.mountPoint
	#

	@property
	def devPath(self) -> str:
		return self.__volume.device.devPath
	#

	@property
	def archiveDirPath(self) -> str:
		return self.__archiveDirPath
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"identifier",
			"volume",
			"inUseFlag",
		] + super()._dumpVarNames()
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Invoke this method to prepare for uploading a backup.
	# This method will check if there is enough disk space available and - if so - provide a temporary upload directory.
	#
	# @return		str tempDirPath				Returns a prepared temporary upload directory or <c>None</c> if this archive can not handle the backup.
	#
	@jk_typing.checkFunctionSignature()
	def tryToPrepareForBackup(self, dt:datetime.datetime, systemName:str, backupUserName:str, backupIdentifier:str, nMaxSizeOfBackup:int) -> str:
		# ensure that this archive is open for writing
		if not self.isReadWrite:
			return None

		nFree = self.__volume.fileSystemStats.bytesFreeUser
		if nMaxSizeOfBackup > nFree:
			return None

		tempDirPath = self._generateTempDirPath(dt, systemName, backupUserName, backupIdentifier)
		self._ioContext.ensureDirExists(tempDirPath)
		self._ioContext.setDirMode(tempDirPath)
		return tempDirPath
	#

	#
	# Move the data provided in a temporary directory into the archive.
	#
	@jk_typing.checkFunctionSignature()
	def acceptIncomingBackup(self, tempDirPath:str, backupInfoFile:ArchivedBackupInfoFile, dataFileNames:list, metaFileNames:list, log:jk_logging.AbstractLogger):
		# ensure that this archive is open for writing
		if not self.isReadWrite:
			return None

		# ensure that the temporary directory provided is owned by this archive
		s = self.tempDirPath
		if not s.endswith(os.path.sep):
			s += os.path.sep
		assert tempDirPath.startswith(s)

		# write the info file
		infoFilePath = os.path.join(tempDirPath, "_backup_info.json")
		backupInfoFile.writeToFile(infoFilePath)

		# generate the real target directory
		dataDirPath = self._generateDataDirPath(
			dt=backupInfoFile.getValue("tBackupStart").dateTime,
			systemName=backupInfoFile.getValue("systemName"),
			backupUserName=backupInfoFile.getValue("backupUserName"),
			backupIdentifier=backupInfoFile.getValue("backupIdentifier")
		)

		# move the whole directory
		if os.path.isdir(dataDirPath):
			self._ioContext.removeDir(dataDirPath)
		os.rename(tempDirPath, dataDirPath)

		# clean internal cach(es)
		self.invalidate()
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	@staticmethod
	@jk_typing.checkFunctionSignature()
	def hasDataStore(volume:BackupVolumeInfo):
		archiveDirPath = os.path.join(volume.backupBaseDirPath, "THANIYA-ARCHIVE")
		return os.path.isdir(archiveDirPath)
	#

#















