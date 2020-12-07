


import os
import datetime

import jk_utils

from .AbstractTargetDirectoryStrategy import AbstractTargetDirectoryStrategy
from .ILocalBackupOriginInfo import ILocalBackupOriginInfo




class TargetDirectoryStrategy_DateDefault(AbstractTargetDirectoryStrategy):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, extraSubDirPath:str = None):
		if extraSubDirPath is not None:
			assert isinstance(extraSubDirPath, str)
			assert extraSubDirPath
			assert extraSubDirPath[0] != "/"
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
		if self.__extraSubDirPath:
			ret = self.__extraSubDirPath
			if not ret.endswith("/"):
				ret += "/"
		else:
			ret = ""

		ret += os.path.join(
			originInfo.localHostName,
			originInfo.currentUserName,
			"{:04d}".format(originInfo.backupDateTime.year),
			"{:04d}-{:02d}-{:02d}".format(originInfo.backupDateTime.year, originInfo.backupDateTime.month, originInfo.backupDateTime.day),
			originInfo.backupIdentifier,
			)
		return ret
	#

#

