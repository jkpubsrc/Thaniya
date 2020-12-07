



import jk_sysinfo
from jk_cachefunccalls import cacheCalls




#
# This is a low level class used by <c>DeviceIterator</c>.
# Use <c>DeviceIterator</c> instead.
#
class _RawDeviceIterator(object):

	################################################################################################################################
	## Static Helper Methods
	################################################################################################################################

	#
	# This method checks if a device is suitable in general for being a backup device.
	# This method excludes ROM devices and snap-devices as well as devices without file system.
	#
	@staticmethod
	def __isSuitableMountedDevice(jDev:dict) -> bool:
		sType = jDev["type"]
		if sType and (sType == "rom"):
			# this is a CD rom or similar => unusable
			return False

		sMountpoint = jDev["mountpoint"]
		if sMountpoint is None:
			# this volume is not mounted
			return False
		if sMountpoint.startswith("/snap/"):
			# this is a snap or similar => unusable
			return False

		if ("children" in jDev) and (jDev["children"] is not None):
			# this device has partions -> do not use it
			return False

		sFSType = jDev["fstype"]
		if sFSType is None:
			# this device has no file system -> do not use it
			return False

		return True
	#

	@staticmethod
	def __isSuitableNonMountedDevice(jDev:dict) -> bool:
		sType = jDev["type"]
		if sType and (sType == "rom"):
			# this is a CD rom or similar => unusable
			return False

		sMountpoint = jDev["mountpoint"]
		if sMountpoint is not None:
			# this is mounted => not a non-mounted device
			return False

		if ("children" in jDev) and (jDev["children"] is not None):
			# this device has partions -> do not use it
			return False

		sFSType = jDev["fstype"]
		if (sFSType is not None) and (sFSType != "crypto_LUKS"):
			# this device has no file system -> do not use it
			return False

		return True
	#

	@staticmethod
	def __iterate(jItems:list, analyzeDeviceCallback):
		for jDev in jItems:

			if analyzeDeviceCallback(jDev):
				yield jDev

			if "children" in jDev:
				yield from _RawDeviceIterator.__iterate(jDev["children"], analyzeDeviceCallback)
	#

	@staticmethod
	def __listMountedDevices(listDevTree:list) -> list:
		ret = []

		if listDevTree is None:
			listDevTree = jk_sysinfo.get_lsblk()["deviceTree"]

		for d in _RawDeviceIterator.__iterate(
				listDevTree,
				_RawDeviceIterator.__isSuitableMountedDevice,
			):
			d["isMounted"] = True
			ret.append(d)

		return ret
	#

	@staticmethod
	def __listNonMountedDevices(listDevTree:list) -> list:
		ret = []

		if listDevTree is None:
			listDevTree = jk_sysinfo.get_lsblk()["deviceTree"]

		for d in _RawDeviceIterator.__iterate(
				listDevTree,
				_RawDeviceIterator.__isSuitableNonMountedDevice,
			):
			d["isMounted"] = False
			ret.append(d)

		return ret
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	#
	# List all devices that are mounted and could theoretically being a backup volume.
	#
	# @return		dict[]		This method will return a list of dictionaries. Each dictionary contains data filled with data parsed from <c>lsblk</c>.
	#
	@staticmethod
	@cacheCalls(seconds=2)
	def listMountedDevices() -> list:
		listDevTree = jk_sysinfo.get_lsblk()["deviceTree"]
		return _RawDeviceIterator.__listMountedDevices(listDevTree)
	#

	#
	# List all non-mounted devices that might be suitable for being a backup volume.
	#
	# @return		dict[]		This method will return a list of dictionaries. Each dictionary contains data filled with data parsed from <c>lsblk</c>.
	#
	@staticmethod
	@cacheCalls(seconds=2)
	def listNonMountedDevices() -> list:
		listDevTree = jk_sysinfo.get_lsblk()["deviceTree"]
		return _RawDeviceIterator.__listNonMountedDevices(listDevTree)
	#

	@staticmethod
	@cacheCalls(seconds=2)
	def listDevices() -> tuple:
		listDevTree = jk_sysinfo.get_lsblk()["deviceTree"]
		return (
			_RawDeviceIterator.__listMountedDevices(listDevTree),
			_RawDeviceIterator.__listNonMountedDevices(listDevTree),
		)
	#

#










