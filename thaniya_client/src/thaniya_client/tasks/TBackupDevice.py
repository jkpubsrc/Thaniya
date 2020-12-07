


import os
import typing

import jk_pathpatternmatcher2
import jk_utils
from jk_typing import checkFunctionSignature
import jk_mounting

from ..ThaniyaBackupContext import ThaniyaBackupContext
from ..ThaniyaIO import ThaniyaIO
from ..tools.EnumTarPathMode import EnumTarPathMode
from ..tools.ThaniyaTar import ThaniyaTar

from .AbstractThaniyaTask import AbstractThaniyaTask






#
# This class performs a backup of a Linux/UNIX block device.
#
class TBackupDevice(AbstractThaniyaTask):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@checkFunctionSignature()
	def __init__(self, devicePath:str, targetFileName:typing.Union[str,None] = None, ensureNotMounted:bool = False):
		assert devicePath
		assert os.path.exists(devicePath)
		assert os.path.isabs(devicePath)
		assert devicePath.startswith("/dev/")

		assert isinstance(ensureNotMounted, bool)
		self.__ensureNotMounted = ensureNotMounted

		if targetFileName is not None:
			assert targetFileName

		self.__devicePath = devicePath

		if targetFileName:
			self.__targetFileName = targetFileName
		else:
			self.__targetFileName = devicePath.replace("/", "-")
			if self.__targetFileName.startswith("-"):
				self.__targetFileName = self.__targetFileName[1:]
			self.__targetFileName = "device--" + self.__targetFileName + ".rawdev"
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def logMessageCalculateSpaceRequired(self) -> str:
		return "Determining backup size of device: " + repr(self.__devicePath)
	#

	@property
	def logMessagePerformBackup(self) -> str:
		return "Performing backup of device: " + repr(self.__devicePath)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def calculateSpaceRequired(self, ctx:ThaniyaBackupContext) -> int:
		nSize = ThaniyaIO.getSizeOfDevice(ctx, self.__devicePath)
		ctx.log.info("I/O expected: " + jk_utils.formatBytes(nSize))
		return nSize
	#

	def performBackup(self, ctx:ThaniyaBackupContext):
		if self.__ensureNotMounted:
			mi = jk_mounting.Mounter().getMountInfoByFilePath(self.__devicePath)
			if mi is not None:
				raise Exception("The device is still mounted: " + repr(self.__devicePath))

		ThaniyaIO.copyDevice(
			ctx=ctx,
			sourceDevicePath=self.__devicePath,
			targetFileOrDirectoryPath=ctx.absPath(self.__targetFileName),
			)
	#

#














