


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
from .server.ThaniyaServerAPIConnectorV1 import ThaniyaServerAPIConnectorV1







#
# NOTE: For this connector to work the user running this program needs to have <c>sudo</c> rights for invoking <c>umount</c>.
#
class BackupConnector_ThaniyaSFTPMount(AbstractBackupConnector, BackupConnectorMixin_mountSFTP, BackupConnectorMixin_unmount):

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

		self._thaniya_host = parameters["thaniya_host"]
		self._thaniya_tcpPort = parameters.get("thaniya_port", 22)
		self._thaniya_login = parameters["thaniya_login"]
		self._thaniya_apiPassword = parameters["thaniya_apiPassword"]

		with ctx.descend("Contacting Thaniya server to allocate backup slot ...") as log2:
			con = ThaniyaServerAPIConnectorV1(self._thaniya_host, self._thaniya_tcpPort)
			con.authenticate(self._thaniya_login, self._thaniya_apiPassword)

			jSlotData = con.allocateSlot(nExpectedNumberOfBytesToWrite)

			self._thaniya_uploadSlotID = jSlotData["slotID"]
			log2.notice("Received: slotID = " + jSlotData["slotID"])

			self._thaniya_uploadHost = jSlotData["ipaddr"]
			log2.notice("Received: ipaddr = " + jSlotData["ipaddr"])

			self._thaniya_uploadPort = jSlotData["port"]
			log2.notice("Received: port = " + str(jSlotData["port"]))

			self._thaniya_uploadLogin = jSlotData["login"]
			log2.notice("Received: login = " + jSlotData["login"])

			self._thaniya_uploadPwd = jSlotData["pwd"]
			log2.notice("Received: pwd = ....")

			self._thaniya_uploadMountDirPath = jSlotData["mountDir"]
			log2.notice("Received: mountDir = " + jSlotData["mountDir"])

		ctx.log.info("Mounting sftp::{}@{}:{} at {} ...".format(self._thaniya_uploadLogin, self._thaniya_uploadHost, self._thaniya_uploadMountDirPath, self.__localMountDirPath))
		self._mountSSH(self.__localMountDirPath, self._thaniya_uploadHost, self._thaniya_uploadPort, self._thaniya_uploadLogin, self._thaniya_uploadPwd, self._thaniya_uploadMountDirPath)
		ctx.log.notice("Mounted.")

		self.__bIsMounted = True
	#

	@jk_typing.checkFunctionSignature()
	def deinitialize(self, ctx:ThaniyaBackupContext) -> bool:
		if not self.__bIsMounted:
			return True

		# ----

		bResult = True

		# signal the server about success or failure

		try:
			with ctx.log.descend("Signaling '{}' to Thaniya server ...".format("error" if ctx.hasError else "success")) as log2:
				con = ThaniyaServerAPIConnectorV1(self._thaniya_host, self._thaniya_tcpPort)
				con.authenticate(self._thaniya_login, self._thaniya_apiPassword)
				con.uploadCompleted(self._thaniya_uploadSlotID, not ctx.hasError)
		except:
			# swallow any exception; it has been logged anyway; we need to contiue;
			bResult = False
			pass

		# now unmount

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












