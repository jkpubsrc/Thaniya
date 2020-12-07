


import os

from .AbstractTargetDirectoryStrategy import AbstractTargetDirectoryStrategy
from .ILocalBackupOriginInfo import ILocalBackupOriginInfo






class TargetDirectoryStrategy_None(AbstractTargetDirectoryStrategy):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		pass
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
		return ""
	#

#

