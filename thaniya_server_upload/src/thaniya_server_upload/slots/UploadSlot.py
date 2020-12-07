


import os
import typing
import time
import datetime

import jk_typing
import jk_utils
import jk_prettyprintobj
import jk_logging
import jk_cachefunccalls
import jk_sysinfo
import jk_json

from thaniya_server_sudo import SudoScriptResult
from thaniya_server_sudo import SudoScriptRunner
from thaniya_server.sysusers import SystemAccount
from thaniya_server.usermgr import BackupUser
from thaniya_server.usermgr import BackupUserManager
from thaniya_server import ServerBackupUploadInfo

from .IUploadSlotContext import IUploadSlotContext
from .EnumUploadSlotState import EnumUploadSlotState
from ._UploadStateData import _UploadStateData












#
# This class represents an upload slot.
#
class UploadSlot(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self):
		self.__sudoScriptRunner = None					# SudoScriptRunner
		self.__systemAccount = None						# SystemAccount

		self.__state = EnumUploadSlotState.UNKNOWN
		self.__uploadStateData = None					# _UploadStateData

		self.__currentUserName = jk_utils.users.lookup_username()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# The name of the user executing this python program.
	#
	@property
	def currentUserName(self) -> str:
		return self.__currentUserName
	#

	@property
	def isReady(self) -> bool:
		return self.__state == EnumUploadSlotState.READY
	#

	@property
	def state(self) -> EnumUploadSlotState:
		return self.__state
	#

	@property
	def systemAccountName(self) -> str:
		return self.__systemAccount.userName
	#

	@property
	def identifier(self) -> str:
		return self.__systemAccount.userName
	#

	@property
	def isAllocated(self) -> bool:
		return bool(self.__uploadStateData)
	#

	#
	# Get the mount point of the file system this user uses.
	#
	@property
	def fsMountPoint(self) -> str:
		return jk_utils.fsutils.findMountPoint(self.__systemAccount.homeDir)
	#

	@property
	def uploadDirPath(self) -> str:
		return os.path.join(self.__systemAccount.homeDir, "upload")
	#

	#
	# Check if we have a process of this user that makes use of <c>mysecureshell</c>. If so a client is still connected.
	#
	# The data of this property is cached for 5 seconds.
	#
	@property
	@jk_cachefunccalls.cacheCalls(seconds=5)
	def isInUseByClient(self) -> bool:
		for x in jk_sysinfo.get_ps():
			if (x["user"] == self.__systemAccount.userName) and (x["cmd"] == "mysecureshell"):
				# we have found the process
				return True
		return False
	#

	#
	# Check if we have a process of this user that makes use of <c>mysecureshell</c>. If so a client is still connected.
	#
	# The data of this property is NOT cached for 5 seconds.
	#
	@property
	def isInUseByClientNoCaching(self) -> bool:
		for x in jk_sysinfo.get_ps():
			if (x["user"] == self.__systemAccount.userName) and (x["cmd"] == "mysecureshell"):
				# we have found the process
				return True
		return False
	#

	@property
	def allocationTime(self) -> typing.Union[float,None]:
		if self.__uploadStateData:
			return self.__uploadStateData.allocationTime
		return None
	#

	@property
	def completionTime(self) -> typing.Union[float,None]:
		if self.__uploadStateData:
			return self.__uploadStateData.completionTime
		return None
	#

	@property
	def lastUsedByClientTime(self) -> typing.Union[float,None]:
		if self.__uploadStateData:
			return self.__uploadStateData.lastUsedByClientTime
		return None
	#

	@property
	def logMessages(self) -> typing.List[str]:
		if self.__uploadStateData:
			return self.__uploadStateData.log.toList()
		return None
	#

	#
	# Either provide the backup user that allcated this slot or <c>None</c>.
	#
	@property
	def backupUser(self) -> typing.Union[BackupUser,None]:
		if self.__uploadStateData:
			return self.__uploadStateData.backupUser
		return None
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"identifier",
			"systemAccountName",
			"state",
			"isAllocated",
			"uploadDirPath",
			"isInUseByClient",
			"allocationTime",
			"completionTime",
			"lastUsedByClientTime",
		]
	#

	################################################################################################################################
	## Serialization Methods
	################################################################################################################################

	def serialize(self, ctx:IUploadSlotContext) -> dict:
		assert isinstance(ctx, IUploadSlotContext)

		return {
			"systemUser": self.__systemAccount.userName,
			"state": str(self.__state),
			"uploadStateData": self.__uploadStateData.toJSON() if self.__uploadStateData else None,
		}
	#

	def initialize(self, ctx:IUploadSlotContext, systemAccount:SystemAccount):
		self.__sudoScriptRunner = ctx.sudoScriptRunner
		self.__systemAccount = systemAccount
		self.__state = EnumUploadSlotState.READY
		self.__uploadStateData = None
	#

	def deserialize(self, ctx:IUploadSlotContext, jData:dict):
		assert isinstance(ctx, IUploadSlotContext)

		self.__sudoScriptRunner = ctx.sudoScriptRunner
		self.__systemAccount = ctx.systemAccountManager.getE(jData["systemUser"])
		self.__state = EnumUploadSlotState.parse(jData["state"])
		if jData["uploadStateData"]:
			self.__uploadStateData = _UploadStateData.fromJSON(jData["uploadStateData"], ctx.backupUserManager)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Check the system if this slot is currently in use. If so remember this information by updating <c>lastUsedByClientTime</c>.
	# This method is called by the <c>UploadSlotManager</c> from within <c>cleanup()</c>.
	#
	def updateUploadStateData(self):
		if self.__state in [ EnumUploadSlotState.UPLOADING ]:
			if self.isInUseByClient:
				self.__uploadStateData.lastUsedByClientTime = time.time()
	#

	@jk_typing.checkFunctionSignature()
	def allocate(self, backupUser:BackupUser, peerNetworkAddress:str, estimatedTotalBytesToUpload:typing.Union[int,None]) -> dict:
		if self.__state not in [ EnumUploadSlotState.READY ]:
			raise Exception("State error: {}".format(self.__state))

		# --------------------------------

		# a) set random password for system account and b) build upload state data record

		usd = _UploadStateData()
		usd.peerNetworkAddress = peerNetworkAddress
		usd.systemUserPwd = self.__systemAccount.setRandomPassword()
		usd.backupUser = backupUser
		usd.allocationTime = time.time()
		usd.lastUsedByClientTime = usd.allocationTime
		usd.estimatedTotalBytesToUpload = estimatedTotalBytesToUpload
		usd.log.info("Slot allocated for: {} @ {}".format(backupUser.userName, peerNetworkAddress))

		# remember this data

		self.__uploadStateData = usd
		self.__state = EnumUploadSlotState.UPLOADING
		self.store()

		# build return data structure

		return {
			"tStart": usd.allocationTime,
			"pwd": usd.systemUserPwd,
			"login": self.__systemAccount.userName,
			"mountDir": "/",
			"uploadDir": "upload",
			"slotID": self.identifier,
		}
	#

	def completed(self):
		if self.__state not in [ EnumUploadSlotState.FINALIZING ]:
			raise Exception("State error: {}".format(self.__state))

		# --------------------------------

		self.log(jk_logging.EnumLogLevel.SUCCESS, "Completed.")

		self.__state = EnumUploadSlotState.COMPLETED
		self.store()
	#

	#
	# Remember the time stamp, disable the account and set the state to FINALIZING.
	#
	def finalizing(self):
		if self.__state not in [ EnumUploadSlotState.UPLOADING ]:
			raise Exception("State error: {}".format(self.__state))

		# --------------------------------

		self.log(jk_logging.EnumLogLevel.SUCCESS, "Finalizing.")

		self.__uploadStateData.completionTime = time.time()

		self.__systemAccount.disable()

		self.__state = EnumUploadSlotState.FINALIZING
		self.store()
	#

	#
	# Reset the account by deleting all files and directories and setting the state to READY.
	# If this fails the account is degraded automatically.
	#
	@jk_typing.checkFunctionSignature()
	def reset(self, log:jk_logging.AbstractLogger = None):
		self.__systemAccount.disable()

		r = self.__sudoScriptRunner.run1(
			scriptName = "account_cleandir",
			argument1 = self.__systemAccount.thaniyaUserNo,
		)

		if r.isError:
			if log:
				r.dump(printFunc=log.notice)
			self.degrade()
			raise Exception("Unknown error encountered cleaning the user's home directory! {}".format(self.__systemAccount.userName))

		self.__uploadStateData = None

		self.__state = EnumUploadSlotState.READY
		self.store()
	#

	def degrade(self):
		try:
			self.__systemAccount.disable()
		except:
			pass

		self.__state = EnumUploadSlotState.DEGRADED
		self.store()
	#

	def timeout(self):
		if self.__state not in [ EnumUploadSlotState.UPLOADING ]:
			raise Exception("State error: {}".format(self.__state))

		# --------------------------------

		self.log(jk_logging.EnumLogLevel.ERROR, "Timeout.")

		try:
			self.__systemAccount.disable()
		except:
			pass

		self.__state = EnumUploadSlotState.TIMEOUT
		self.store()
	#

	#
	# Move all files from within the upload (!!) directory to a subdirectory in the upload target directory.
	# This is done invoking a sudo script. (The script will create a suitable subdirectory in the upload target directory by itself and report it.)
	# If this fails the account is degraded automatically.
	#
	# TODO: If this method fails the slot should degrade automatically. Can this somehow be automated in a reasonable form? without swallowing the exception?
	#		(the caller should learn about possible problems that occurred!)
	#
	# @return		str clientUploadDataDirPath				The directory where the uploaded client data has been stored
	#
	@jk_typing.checkFunctionSignature()
	def moveFilesToSpoolDirAndReset(self, log:jk_logging.AbstractLogger) -> str:
		if self.__state not in [ EnumUploadSlotState.COMPLETED ]:
			raise Exception("State error: {}".format(self.__state))

		assert self.__systemAccount.isDisabled

		# --------------------------------

		r = self.__sudoScriptRunner.run2(
			scriptName = "account_movefiles",
			argument1 = self.__systemAccount.thaniyaUserNo,
			argument2 = self.__currentUserName,
		)

		if r.isError or not r.stdOutLines:
			r.dump(printFunc=log.notice)
			self.degrade()
			raise Exception("Unknown error encountered moving upload files from account: {}".format(self.__systemAccount.userName))

		clientUploadDataDirPath = r.stdOutLines[0]

		# now write the server information file

		log.notice("Writing server information about the uploaded backup ...")

		# TODO: check to what extent we can use the _UploadStateData.toJSON() method itself
		sbui = ServerBackupUploadInfo()
		sbui.data.setValue("backupUser", self.__uploadStateData.backupUser.userName)
		sbui.data.setValue("tAllocation", self.__uploadStateData.allocationTime)
		sbui.data.setValue("tCompletion", self.__uploadStateData.completionTime)
		sbui.data.setValue("peerNetworkAddress", self.__uploadStateData.peerNetworkAddress)
		sbui.data.setValue("estimatedTotalBytesToUpload", self.__uploadStateData.estimatedTotalBytesToUpload)
		sbui.data.setValue("rawLog", self.__uploadStateData.log.toList())
		sbui.writeToDir(clientUploadDataDirPath)

		# cleanup the slot: remove everything

		self.reset(log)

		return clientUploadDataDirPath
	#

	def log(self, logLevel:jk_logging.EnumLogLevel, logMsg:str):
		assert isinstance(logLevel, jk_logging.EnumLogLevel)
		assert isinstance(logMsg, str)
		assert logMsg

		# --------------------------------

		if self.__uploadStateData is None:
			raise Exception("State error: {}".format(self.__state))

		# --------------------------------

		self.__uploadStateData.log.log(logLevel, logMsg)
		self.store()
	#

#


















