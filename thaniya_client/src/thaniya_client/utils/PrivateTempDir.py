








import stat
import os
import tempfile
import weakref
import shutil
import warnings
import typing
import random

import jk_utils








class PrivateTempDir(object):

	__CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

	__FILE_MODE = jk_utils.ChModValue("rw-------").toInt()
	__DIR_MODE = jk_utils.ChModValue("rwx------").toInt()

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, baseDirPath:str):
		assert isinstance(baseDirPath, str)
		assert os.path.isdir(baseDirPath)
		assert os.path.isabs(baseDirPath)

		self.__tempDirPath = tempfile.mkdtemp(".tmp", "tmp", baseDirPath)

		assert os.stat(self.__tempDirPath).st_mode == PrivateTempDir.__DIR_MODE | 16384

		self._finalizer = weakref.finalize(
			self,
			self.__cleanup,
			self.__tempDirPath,
			warn_message="Implicitly cleaning up {!r}".format(self))
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __newPath(self) -> str:
		while True:
			tempDirName = "".join([ random.choice(PrivateTempDir.__CHARS) for x in range(0, 32) ])
			path = os.path.join(self.__tempDirPath, tempDirName)
			if not os.path.exists(path):
				return path
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def createDirectory(self) -> str:
		path = self.__newPath()

		os.mkdir(path, PrivateTempDir.__DIR_MODE)

		return path
	#

	#
	# Create a new text file with content. The file is cleaned up automatically as soon as this private
	# temporary directory is removed.
	#
	def writeTextFile(self, text:str) -> str:
		assert isinstance(text, str)

		path = self.__newPath()

		with open(os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, PrivateTempDir.__FILE_MODE), "w") as f:
			f.write(text)

		return path
	#

	#
	# Create a new binary file with content. The file is cleaned up automatically as soon as this private
	# temporary directory is removed.
	#
	def writeBinaryFile(self, data:typing.Union[bytes,bytearray]) -> str:
		assert isinstance(data, (bytes, bytearray))

		path = self.__newPath()

		with open(os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, PrivateTempDir.__FILE_MODE), "wb") as f:
			f.write(data)

		return path
	#

	@classmethod
	def __cleanup(cls, tempDirPath:str, warn_message):
		shutil.rmtree(tempDirPath)
		warnings.warn(warn_message, ResourceWarning)
	#

	def __repr__(self):
		return "<{} {!r}>".format(self.__class__.__name__, self.__tempDirPath)
	#

	def __enter__(self):
		return self
	#

	def __exit__(self, exc, value, tb):
		self.cleanup()
	#

	def cleanup(self):
		if self._finalizer.detach():
			shutil.rmtree(self.__tempDirPath)
	#

#









