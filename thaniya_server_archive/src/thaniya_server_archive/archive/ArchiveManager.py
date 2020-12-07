



import os
import typing
import datetime

import jk_typing
import jk_utils
import jk_logging
import jk_prettyprintobj

from thaniya_common.utils import IOContext

from ..volumes.BackupVolumeID import BackupVolumeID
from ..volumes.BackupVolumeInfo import BackupVolumeInfo

from .ArchiveDataStore import ArchiveDataStore








class ArchiveManager(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self):
		self.__ioContext = IOContext()
		self.__archives = []
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def archives(self) -> typing.Tuple[ArchiveDataStore]:
		return tuple(self.__archives)
	#

	@property
	def backupVolumesUsed(self) -> typing.List[BackupVolumeID]:
		return [
			a.identifer for a in self.__archives
		]
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"archives",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def register(self, volume:BackupVolumeInfo, bReadWrite:bool, log:jk_logging.AbstractLogger) -> ArchiveDataStore:
		assert volume.isValid
		assert volume.isActive

		_s = " (readonly) ..." if bReadWrite else " ..."
		if ArchiveDataStore.hasDataStore(volume):
			with log.descend("Opening existing archive" + _s) as log2:
				a = ArchiveDataStore(self.__ioContext, volume, bReadWrite, log2)
		else:
			with log.descend("Creating new archive" + _s) as log2:
				a = ArchiveDataStore(self.__ioContext, volume, bReadWrite, log2)

		self.__archives.append(a)

		return a
	#

	@jk_typing.checkFunctionSignature()
	def get(self, backupVolumeID:BackupVolumeID) -> typing.Union[ArchiveDataStore,None]:
		for a in self.__archives:
			if a.identifier == backupVolumeID:
				return a
		return None
	#

	@jk_typing.checkFunctionSignature()
	def hasArchive(self, backupVolumeID:BackupVolumeID) -> bool:
		for a in self.__archives:
			if a.identifier == backupVolumeID:
				return True
		return False
	#

	#
	# Invoke this method to get an archive for uploading a backup.
	# This method will check if ...
	# * there is an archive,
	# * there is enough disk space available in that archive,
	# * and provide a temporary upload directory from that archive.
	#
	# @param		str|BackupVolumeID archiveID	(optional) If an archive ID is specified, the framework will try to pick exactly *this* archive.
	#												The reason why this option is required is that uploads that might allready have been performed partially
	#												should go to exactly the same archive again. We try to be indempotent in upload operations, so this
	#												information might be provided.
	#
	# @return		ArchiveDataStore archive		The archive if a suitable archive is found. <c>None</c> is returned otherwise.
	# @return		str tempDirPath					A prepared temporary upload directory if a suitable archive is found. <c>None</c> is returned otherwise.
	#
	@jk_typing.checkFunctionSignature()
	def getArchiveForIncomingBackup(self,
			dt:datetime.datetime,
			systemName:str,
			backupUserName:str,
			backupIdentifier:str,
			nMaxSizeOfBackup:int,
			archiveID:typing.Union[str,BackupVolumeID,None]
		) -> typing.Tuple[ArchiveDataStore,str]:

		if archiveID is not None:
			if isinstance(archiveID, str):
				backupVolumeID = BackupVolumeID.parseFromHexStr(archiveID)

			for a in self.__archives:
				if a.identifer == backupVolumeID:
					tempDirPath = a.tryToPrepareForBackup(
						dt=dt,
						systemName=systemName,
						backupUserName=backupUserName,
						backupIdentifier=backupIdentifier,
						nMaxSizeOfBackup=nMaxSizeOfBackup
					)
					if tempDirPath:
						return a, tempDirPath

		else:
			for a in self.__archives:
				tempDirPath = a.tryToPrepareForBackup(
					dt=dt,
					systemName=systemName,
					backupUserName=backupUserName,
					backupIdentifier=backupIdentifier,
					nMaxSizeOfBackup=nMaxSizeOfBackup
				)
				if tempDirPath:
					return a, tempDirPath

		return None, None
	#

#











