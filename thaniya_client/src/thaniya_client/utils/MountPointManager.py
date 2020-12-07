








import stat
import os
import tempfile
import weakref
import shutil
import warnings
import random

import jk_utils

from .MountPointRandom import MountPointRandom







class MountPointManager(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, baseDirPath:str = None):
		if baseDirPath is None:
			baseDirPath = "/tmp"
		assert os.path.isdir(baseDirPath)

		self.__baseDirPath = baseDirPath
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# This method generates a random directory suitable for mounting. The directory is set to "rwx------" so that only the current user
	# will be able to read and write to this directory.
	#
	def createMountPoint(self) -> MountPointRandom:
		return MountPointRandom(self.__baseDirPath)
	#

#









