



import typing

from jk_cachefunccalls import cacheCalls

from .Device import Device
from ._RawDeviceIterator import _RawDeviceIterator






#
# Iterates over information of devices and returns <c>Device</c> instances accordingly.
# This is the high level interface in opposition to the low level interface <c>_RawDeviceIterator</c>.
#
class DeviceIterator(object):

	################################################################################################################################
	## Static Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	#
	# List all devices that are mounted and could theoretically being a backup volume.
	#
	# @return		Device[]		This method will return a list of <c>Device</c> objects. Each dictionary contains data filled with data parsed from <c>lsblk</c>.
	#
	@staticmethod
	@cacheCalls(seconds=2)
	def listMountedDevices() -> typing.List[Device]:
		return [
			Device.createFromLsBlk(x) for x in _RawDeviceIterator.listMountedDevices()
		]
	#

	#
	# List all non-mounted devices that might be suitable for being a backup volume.
	#
	# @return		Device[]		This method will return a list of <c>Device</c> objects. Each dictionary contains data filled with data parsed from <c>lsblk</c>.
	#
	@staticmethod
	@cacheCalls(seconds=2)
	def listNonMountedDevices() -> typing.List[Device]:
		return [
			Device.createFromLsBlk(x) for x in _RawDeviceIterator.listNonMountedDevices()
		]
	#

	@staticmethod
	@cacheCalls(seconds=2, dependArgs=[0])
	def getNonMountedDevice(path:str) -> typing.Union[Device,None]:
		for d in DeviceIterator.listNonMountedDevices():
			if (d.devPath == path) or (d.mountPoint == path):
				return d
		return None
	#

	@staticmethod
	@cacheCalls(seconds=2, dependArgs=[0])
	def getMountedDevice(path:str) -> typing.Union[Device,None]:
		for d in DeviceIterator.listMountedDevices():
			if (d.devPath == path) or (d.mountPoint == path):
				return d
		return None
	#

	#
	# @return		Device[]		Return a list of mounted devices. Each dictionary contains data filled with data parsed from <c>lsblk</c>.
	# @return		Device[]		Return a list of non-mounted devices. Each dictionary contains data filled with data parsed from <c>lsblk</c>.
	#
	@staticmethod
	@cacheCalls(seconds=2)
	def listDevices() -> tuple:
		mountDevs, nonMountDevs = _RawDeviceIterator.listDevices()
		return (
			[
				Device.createFromLsBlk(x) for x in mountDevs
			],
			[
				Device.createFromLsBlk(x) for x in nonMountDevs
			],
		)
	#

#










