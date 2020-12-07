


import os
import typing

import jk_typing
import jk_prettyprintobj
import jk_utils

from .BackupVolumeID import BackupVolumeID
from .Device import Device
from .BackupVolumeCfgFile import BackupVolumeCfgFile
from .DeviceIterator import DeviceIterator






#
# This class is an informational class. It provides information about backup volumes.
#
class BackupVolumeInfo(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, mgr, volumeCfgType:str, device:Device, backupVolumeID:BackupVolumeID, backupBaseDirPath:str, backupVolumeCfgFilePath:str):
		self.__mgr = mgr
		self.__device = device
		self.__backupBaseDirPath = backupBaseDirPath
		self.__backupVolumeID = backupVolumeID
		self.__volumeCfgType = volumeCfgType
		self.__backupVolumeCfgFilePath = backupVolumeCfgFilePath
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def backupVolumeCfgFilePath(self) -> str:
		return self.__backupVolumeCfgFilePath
	#

	@property
	def device(self) -> typing.Union[Device,None]:
		return self.__device
	#

	@property
	def backupBaseDirPath(self) -> str:
		return self.__backupBaseDirPath
	#

	@property
	def volumeCfgType(self) -> str:
		return self.__volumeCfgType
	#

	@property
	def backupVolumeID(self) -> BackupVolumeID:
		return self.__backupVolumeID
	#

	@property
	def isValid(self) -> bool:
		return self.__device is not None
	#

	@property
	def isActive(self) -> bool:
		return self.__mgr.isActive(self.__backupVolumeID)
	#

	@property
	def fileSystemStats(self) -> typing.Union[jk_utils.fsutils.FileSystemStats,None]:
		if self.__device is None:
			# TODO: derive mount point from backupBaseDirPath
			return None

		fsStats = jk_utils.fsutils.getFileSystemStats(self.__device.mountPoint)
		assert isinstance(fsStats, jk_utils.fsutils.FileSystemStats)
		return fsStats
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"volumeCfgType",
			"isValid",
			"isActive",
			"device",
			"backupVolumeID",
			"backupBaseDirPath",
			"backupVolumeCfgFilePath",
			"fileSystemStats"
		]
	#

	################################################################################################################################
	## Static Method
	################################################################################################################################

#




