


import time
import os
import subprocess

import jk_utils
import jk_mounting
import jk_typing

from .AbstractBackupConnector import AbstractBackupConnector
from .ThaniyaIO import ThaniyaIO
from .ThaniyaBackupContext import ThaniyaBackupContext
from .BackupConnectorMixin_mountSFTP import BackupConnectorMixin_mountSFTP
from .BackupConnectorMixin_unmount import BackupConnectorMixin_unmount








#
# NOTE: For this connector to work the user running this program needs to have <c>sudo</c> rights for invoking <c>umount</c>.
#
class BackupConnector_SFTPMount(AbstractBackupConnector, BackupConnectorMixin_mountSFTP, BackupConnectorMixin_unmount):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		self.__localMountDirPath = None
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
		return self.__localMountDirPath
	#

	@property
	def baseTargetDirPath(self) -> str:
		return self.__localMountDirPath
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def initialize(self, ctx:ThaniyaBackupContext, nExpectedNumberOfBytesToWrite:int, parameters:dict):
		self.__localMountDirPath = ctx.privateTempDir.createDirectory()

		self._ssh_hostAddress = parameters["ssh_hostAddress"]
		self._ssh_login = parameters["ssh_login"]
		self._ssh_password = parameters["ssh_password"]
		self._ssh_port = parameters.get("ssh_port", 22)
		self._ssh_dirPath = parameters["ssh_dirPath"]

		ctx.log.info("Mounting ssh::{}@{}:{} at {} ...".format(self._ssh_login, self._ssh_hostAddress, self._ssh_dirPath, self.__localMountDirPath))
		self._mountSSH(self.__localMountDirPath, self._ssh_hostAddress, self._ssh_port, self._ssh_login, self._ssh_password, self._ssh_dirPath)
		ctx.log.notice("Mounted.")

		self.__bIsMounted = True
	#

	@jk_typing.checkFunctionSignature()
	def deinitialize(self, ctx:ThaniyaBackupContext) -> bool:
		if not self.__bIsMounted:
			return True

		# ----

		bResult = True

		# unmount

		with ctx.log.descend("Unmounting ...") as log2:
			lastException = self._tryRepeatedUnmount(self.__localMountDirPath, 5)			# let's do 5 unmount attempts.
			if lastException is None:
				# success
				self.__bIsMounted = False
			else:
				# failure
				bResult = False
				log2.error(lastException)
				log2.error("Giving up.")

		# ----

		return bResult
	#

	def dump(self):
		print("BackupConnector_SFTPMount")
		#for key in [ "_sessionID",
		#	"mountPoint" ]:
		#	print("\t" + key, "=", getattr(self, key))
	#

#












