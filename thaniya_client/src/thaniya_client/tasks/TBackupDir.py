


import os

import jk_pathpatternmatcher2
import jk_utils
from jk_typing import checkFunctionSignature

from ..ThaniyaBackupContext import ThaniyaBackupContext
from ..tools.EnumTarPathMode import EnumTarPathMode
from ..tools.ThaniyaTar import ThaniyaTar

from .AbstractThaniyaTask import AbstractThaniyaTask





#
# This class performs a backup of a single directory with all it's content (recursively).
#
class TBackupDir(AbstractThaniyaTask):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@checkFunctionSignature()
	def __init__(self, sourceDirPath:str):
		assert sourceDirPath
		if not os.path.isdir(sourceDirPath):
			raise Exception("No such directory: " + sourceDirPath)
		if not os.path.isabs(sourceDirPath):
			raise Exception("Not an absolute path: " + sourceDirPath)

		self.__sourceDirPath = sourceDirPath

		self.__targetFileName = sourceDirPath.replace("/", "-").replace("\\", "-") + ".tar"
		if self.__targetFileName.startswith("-"):
			self.__targetFileName = self.__targetFileName[1:]
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def logMessageCalculateSpaceRequired(self) -> str:
		return "Calculating backup size of directory: " + repr(self.__sourceDirPath)
	#

	@property
	def logMessagePerformBackup(self) -> str:
		return "Performing backup of directory: " + repr(self.__sourceDirPath)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@checkFunctionSignature()
	def calculateSpaceRequired(self, ctx:ThaniyaBackupContext) -> int:
		nErrors, nSize = ThaniyaTar.tarCalculateSize(
			ctx=ctx,
			walker=jk_pathpatternmatcher2.walk(self.__sourceDirPath)
			)

		ctx.log.info("I/O expected: " + jk_utils.formatBytes(nSize))

		return nSize
	#

	@checkFunctionSignature()
	def performBackup(self, ctx:ThaniyaBackupContext):

		def errorCallback(entry:jk_pathpatternmatcher2.Entry, exception):
			ctx.log.warn(str(exception))
			#ctx.log.error(str(exception))
		#

		ThaniyaTar.tar(
			ctx=ctx,
			outputTarFilePath=ctx.absPath(self.__targetFileName),
			walker=jk_pathpatternmatcher2.walk(self.__sourceDirPath),
			pathMode = EnumTarPathMode.RELATIVE_PATH_WITH_BASE_DIR,
			onErrorCallback=errorCallback,
			)
	#

#














