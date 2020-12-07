


import jk_typing

from .ThaniyaBackupContext import ThaniyaBackupContext
from .AbstractBackupConnector import AbstractBackupConnector





class BackupConnector_DebugWrapper(AbstractBackupConnector):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, backupClient:AbstractBackupConnector):
		self.__backupClient = backupClient
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def performsMountUnmount(self) -> bool:
		print("> performsMountUnmount: begin")
		return self.__backupClient.performsMountUnmount
		print("> performsMountUnmount: end")
	#

	@property
	def isReady(self) -> bool:
		print("> isReady: begin")
		return self.__backupClient.isReady
		print("> isReady: end")
	#

	@property
	def mountDirPath(self) -> str:
		print("> mountDirPath: begin")
		return self.__backupClient.mountDirPath
		print("> mountDirPath: end")
	#

	@property
	def baseTargetDirPath(self) -> str:
		print("> baseTargetDirPath: begin")
		return self.__backupClient.baseTargetDirPath
		print("> baseTargetDirPath: end")
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:ThaniyaBackupContext, nExpectedNumberOfBytesToWrite:int, parameters:dict):
		print("> initialize: begin")
		self.__backupClient.initialize(ctx, nExpectedNumberOfBytesToWrite, parameters)
		print("> initialize: end")
	#

	@jk_typing.checkFunctionSignature()
	def deinitialize(self, ctx:ThaniyaBackupContext):
		print("> deinitialize: begin")
		self.__backupClient.deinitialize(ctx)
		print("> initialize: end")
	#

	"""
	def onBackupCompleted(self, bError:bool):
		print("> onBackupCompleted: begin")
		self.__backupClient.onBackupCompleted(bError)
		print("> onBackupCompleted: end")
	#
	"""

	def dump(self):
		print("> dump: begin")
		self.__backupClient.dump()
		print("> dump: end")
	#

#













