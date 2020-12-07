








import stat
import os
import tempfile
import weakref
import shutil
import warnings
import random

import jk_utils








class MountPointRandom(object):

	__CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, baseDirPath:str):
		assert isinstance(baseDirPath, str)
		assert os.path.isdir(baseDirPath)

		self.__tempDirPath = tempfile.mkdtemp(".tmp", "tmp", baseDirPath)

		tempDirName = "".join([ random.choice(MountPointRandom.__CHARS) for x in range(0, 32) ])
		self.__mountDirPath = os.path.join(self.__tempDirPath, tempDirName)
		os.mkdir(self.__mountDirPath, jk_utils.ChModValue("rwx------").toInt())

		assert os.stat(self.__tempDirPath).st_mode == jk_utils.ChModValue("rwx------").toInt() | 16384
		assert os.stat(self.__mountDirPath).st_mode == jk_utils.ChModValue("rwx------").toInt() | 16384

		self._finalizer = weakref.finalize(
			self,
			self.__cleanup,
			self.__tempDirPath,
			warn_message="Implicitly cleaning up {!r}".format(self))
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def dirPath(self) -> str:
		return self.__mountDirPath
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@classmethod
	def __cleanup(cls, tempDirPath:str, warn_message):
		shutil.rmtree(tempDirPath)
		warnings.warn(warn_message, ResourceWarning)
	#

	def __repr__(self):
		return "<{} {!r}>".format(self.__class__.__name__, self.__mountDirPath)
	#

	def __enter__(self):
		return self.__mountDirPath
	#

	def __exit__(self, exc, value, tb):
		self.cleanup()
	#

	def cleanup(self):
		if self._finalizer.detach():
			shutil.rmtree(self.__tempDirPath)
	#

#









