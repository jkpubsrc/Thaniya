


import os

from .AbstractTargetDirectoryStrategy import AbstractTargetDirectoryStrategy
from .ILocalBackupOriginInfo import ILocalBackupOriginInfo






class TargetDirectoryStrategy_StaticDir(AbstractTargetDirectoryStrategy):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, extraSubDirPath:str = None):
		if extraSubDirPath is not None:
			assert isinstance(extraSubDirPath, str)
			assert extraSubDirPath
			assert extraSubDirPath[0] != os.path.sep
		self.__extraSubDirPath = extraSubDirPath
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# This method is invoked in order to receive a valid target directory.
	#
	# @param		ILocalBackupOriginInfo originInfo		Information about the origin of this backup.
	# @return		str										Returns a path which indicates where to write the backup to. This return value will be made part of the absolute path to write data to.
	#
	def selectEffectiveTargetDirectory(self, originInfo:ILocalBackupOriginInfo):
		ret = ""

		if self.__extraSubDirPath:
			ret = self.__extraSubDirPath

		return ret
	#

#

