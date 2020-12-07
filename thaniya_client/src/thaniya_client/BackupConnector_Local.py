


import os

import jk_utils
import jk_typing

from .AbstractBackupConnector import AbstractBackupConnector
from .ThaniyaIO import ThaniyaIO
from .ThaniyaBackupContext import ThaniyaBackupContext





class BackupConnector_Local(AbstractBackupConnector):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		self.__baseTargetDirPath = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def isReady(self) -> bool:
		return bool(self.__baseTargetDirPath)
	#

	@property
	def baseTargetDirPath(self) -> str:
		return self.__baseTargetDirPath
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:ThaniyaBackupContext, nExpectedNumberOfBytesToWrite:int, parameters:dict):
		self.__baseTargetDirPath = parameters["dirPath"]
	#

	@jk_typing.checkFunctionSignature()
	def deinitialize(self, ctx:ThaniyaBackupContext):
		pass
	#

	def dump(self):
		print("BackupConnector_Local")
		#for key in [ "_sessionID",
		#	"mountPoint" ]:
		#	print("\t" + key, "=", getattr(self, key))
	#

#












