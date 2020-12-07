


import sys
import time
import os
import subprocess
import string
import random

import jk_utils
import jk_mounting
import jk_typing

from .AbstractBackupConnector import AbstractBackupConnector
from .ThaniyaIO import ThaniyaIO
from .ThaniyaBackupContext import ThaniyaBackupContext
from .BackupConnectorMixin_mountCIFS import BackupConnectorMixin_mountCIFS







class BackupConnector_CIFSMount(AbstractBackupConnector, BackupConnectorMixin_mountCIFS):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		self.__mountDirPath = None
		self.__bIsMounted = False
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def performsMountUnmount(self) -> bool:
		return True
	#

	@property
	def isReady(self) -> bool:
		return self.__bIsMounted
	#

	@property
	def mountDirPath(self) -> str:
		return self.__mountDirPath
	#

	@property
	def baseTargetDirPath(self) -> str:
		return self.__mountDirPath
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:ThaniyaBackupContext, nExpectedNumberOfBytesToWrite:int, parameters:dict):
		self.__mountDirPath = ctx.privateTempDir.createDirectory()

		self._cifs_hostAddress = parameters["cifs_hostAddress"]
		self._cifs_login = parameters["cifs_login"]
		self._cifs_password = parameters["cifs_password"]
		#self._cifs_port = parameters.get("cifs_port", 445)
		self._cifs_version = parameters["cifs_version"]
		self._cifs_shareName = parameters["cifs_shareName"]

		ctx.log.info("Mounting cifs::{}@{}:{} at {} ...".format(self._cifs_login, self._cifs_hostAddress, self._cifs_shareName, self.__mountDirPath))
		self._mountCIFS(
			ctx,
			self.__mountDirPath,
			self._cifs_hostAddress,
			#self._cifs_port,
			self._cifs_shareName,
			self._cifs_login,
			self._cifs_password,
			self._cifs_version)
		ctx.log.notice("Mounted.")

		self.__bIsMounted = True
	#

	@jk_typing.checkFunctionSignature()
	def deinitialize(self, ctx:ThaniyaBackupContext):
		if self.__bIsMounted:
			ctx.log.info("Unmounting ...")
			# let's do 5 unmount attempts.
			for i in range(0, 4):
				time.sleep(1)
				try:
					self._umount(self.__mountDirPath)
					ctx.log.notice("Success.")
					self.__bIsMounted = False
					return
				except Exception as ee:
					pass
			time.sleep(1)
			self._umount(self.__mountDirPath)
			ctx.log.error("Giving up.")
	#

	def dump(self):
		print("BackupConnector_CIFSMount")
		#for key in [ "_sessionID",
		#	"mountPoint" ]:
		#	print("\t" + key, "=", getattr(self, key))
	#

#












