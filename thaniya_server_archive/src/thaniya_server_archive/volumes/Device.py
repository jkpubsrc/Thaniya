


import os
import typing

import jk_prettyprintobj
import jk_utils





#
# This class represents a device volume.
# A volume is a drive, a disk or partition or something of that kind: A block device as either part of a piece of hardware or an single equivalent of that piece of hardware.
#
# A device volume does not necessarily be a backup volume. Such a device volume can be a backup volume, but such a device also can contain multiple backup volumes in different locations.
#
# This is a read only object.
#
class Device(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	#
	# @param		str devPath				(required) The device path such as <c>/dev/sda</c>, <c>/dev/sda1</c> or <c>/dev/loop5</c>
	# @param		str mountPoint			(optional) The mount point of this device (or <c>null</c> if not mouted
	# @param		str fsType				(optional) The file system type identifier such as: <c>crypto_LUKS</c>, <c>iso9960</c>, <c>ext4</c>, etc.
	# @param		str uuid				(optional) A unique identifier assigned by the operating system
	# @param		int phySecSizeInBytes	(required) The physical sector size in bytes
	# @param		int sizeInBytes			(required) The size of the volume in bytes
	# @param		str devType				(required) The device type such as: <c>part</c>, <c>rom</c>, <c>loop</c>, etc.
	#
	def __init__(self, devPath:str, mountPoint:str, fsType:str, uuid:str, phySecSizeInBytes:int, sizeInBytes:int, devType:str):
		assert isinstance(devPath, str)
		if mountPoint is not None:
			assert isinstance(mountPoint, str)
		if fsType is not None:
			assert isinstance(fsType, str)
		if uuid is not None:
			assert isinstance(uuid, str)
		assert isinstance(phySecSizeInBytes, int)
		assert isinstance(sizeInBytes, int)
		assert isinstance(devType, str)

		self.__devPath = devPath
		self.__mountPoint = mountPoint
		self.__fsType = fsType
		self.__uuid = uuid
		self.__phySecSizeInBytes = phySecSizeInBytes
		self.__sizeInBytes = sizeInBytes
		self.__devType = devType
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# The device path such as <c>/dev/sda</c>, <c>/dev/sda1</c> or <c>/dev/loop5</c>
	#
	@property
	def devPath(self) -> str:
		return self.__devPath
	#

	#
	# The mount point of this device (or <c>null</c> if not mouted
	#
	@property
	def mountPoint(self) -> typing.Union[str,None]:
		return self.__mountPoint
	#

	#
	# The file system type identifier such as: <c>crypto_LUKS</c>, <c>iso9960</c>, <c>ext4</c>, etc.
	#
	@property
	def fsType(self) -> typing.Union[str,None]:
		return self.__fsType
	#

	#
	# A unique identifier assigned by the operating system
	#
	@property
	def uuid(self) -> typing.Union[str,None]:
		return self.__uuid
	#

	#
	# The physical sector size in bytes
	#
	@property
	def phySecSizeInBytes(self) -> int:
		return self.__phySecSizeInBytes
	#

	#
	# The size of the volume in bytes
	#
	@property
	def sizeInBytes(self) -> int:
		return self.__sizeInBytes
	#

	@property
	def bytesFree(self) -> int:
		statvfs = os.statvfs(self.__mountPoint)
		bytesFreeUser = statvfs.f_frsize * statvfs.f_bavail
		return bytesFreeUser
	#

	#
	# The device type such as: <c>part</c>, <c>rom</c>, <c>loop</c>, etc.
	#
	@property
	def devType(self) -> str:
		return self.__devType
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"devPath",
			"devType",
			"mountPoint",
			"fsType",
			"uuid",
			"phySecSizeInBytes",
			"sizeInBytes",
			"bytesFree",
		]
	#

	def __eq__(self, other):
		if other.__class__ != Device:
			return False
		return other.__devPath == self.devPath
	#

	def __ne__(self, other):
		if other.__class__ != Device:
			return True
		return other.__devPath != self.devPath
	#

	################################################################################################################################
	## Static Method
	################################################################################################################################

	@staticmethod
	def createFromLsBlk(jData:dict):
		return Device(
			jData["dev"],
			jData["mountpoint"],
			jData["fstype"],
			jData["uuid"],
			int(jData["phy-sec"]),
			int(jData["size"]),
			jData["type"],
		)
	#

#




