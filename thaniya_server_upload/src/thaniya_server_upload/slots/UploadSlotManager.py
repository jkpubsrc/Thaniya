


import os
import stat
import typing
import time

import jk_typing
import jk_utils
import jk_simpleobjpersistency
import jk_logging
import jk_cachefunccalls

from thaniya_server_sudo import SudoScriptResult
from thaniya_server_sudo import SudoScriptRunner
from thaniya_server.sysusers import SystemAccount
from thaniya_server.sysusers import SystemAccountManager
from thaniya_server.usermgr import BackupUser
from thaniya_server.usermgr import BackupUserManager
from thaniya_server.utils.APIError import APIError
from thaniya_common.utils import IOContext

from .IUploadSlotContext import IUploadSlotContext
from .EnumUploadSlotState import EnumUploadSlotState
from .UploadSlot import UploadSlot









class _UploadSlotContext(IUploadSlotContext):

	def __init__(self, backupUserManager:BackupUserManager, sudoScriptRunner:SudoScriptRunner, systemAccountManager:SystemAccountManager):
		self.__backupUserManager = backupUserManager
		self.__sudoScriptRunner = sudoScriptRunner
		self.__systemAccountManager = systemAccountManager
	#

	@property
	def backupUserManager(self) -> BackupUserManager:
		return self.__backupUserManager
	#

	@property
	def sudoScriptRunner(self) -> SudoScriptRunner:
		return self.__sudoScriptRunner
	#

	@property
	def systemAccountManager(self) -> SystemAccountManager:
		return self.__systemAccountManager
	#

#






#
# This class manages the system accounts that can be used for uploading via SFTP.
#
# NOTE: If the user account of upload slots reside on different file systems a warning is emitted during initialization and this property will
# then return one mount point of the upload slots (without any definition of which one). So you are adviced to only use one file system for uploaders.
# The reason behind that is that this upload slot manager needs to determine the number of free space. If uploads go to different file systems a much more
# sophisticated disk space management would be required. (For now such a more sophisticated disk space management has not been implemented in this class.)
#
class UploadSlotManager(IUploadSlotContext):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	# @param		IOContext ioContext							An IOContext to use to assist in managing files and directories.
	# @param		BackupUserManager backupUserManager			The user manager of the backup system that manages all user accounts.
	# @param		SudoScriptRunner sudoScriptRunner			A component that allows to run scripts as superuser.
	# @param		str slotStatesDirPath						In this directory the upload slot manager will persistently store states about the slots.
	# @param		str uploadResultDirPath						This directory will receive the uploaded data after uploading has been completed by the client.
	# @param		int nSecuritySpaceMarginBytes				TODO
	# @param		AbstractLogger log							The log facility to write log messages to. This logger is not stored by used for providing information during startup.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self,
			ioContext:IOContext,
			backupUserManager:BackupUserManager,
			sudoScriptRunner:SudoScriptRunner,
			slotStatesDirPath:str,
			uploadResultDirPath:str,
			nSecuritySpaceMarginBytes:int,
			log:jk_logging.AbstractLogger
		):

		self.__ioContext = ioContext

		with log.descend("Initializing slot manager ...") as log2:

			if not os.path.isdir(uploadResultDirPath):
				raise Exception("No such directory: " + uploadResultDirPath)
			if not os.path.isabs(uploadResultDirPath):
				raise Exception("Not an absolute path: " + uploadResultDirPath)

			if not os.path.isdir(slotStatesDirPath):
				raise Exception("No such directory: " + slotStatesDirPath)
			if not os.path.isabs(slotStatesDirPath):
				raise Exception("Not an absolute path: " + slotStatesDirPath)

			assert uploadResultDirPath != slotStatesDirPath

			# ----

			log2.notice("Using result directory: " + uploadResultDirPath)
			self.__uploadResultDirPath = uploadResultDirPath
			self.__fileSystemMountPoint = jk_utils.fsutils.findMountPoint(uploadResultDirPath)

			# ensure restricted access
			self.__ioContext.setDirMode(uploadResultDirPath)
			# TODO: check if this directory is owned by the user under which the current program is runing

			# ----

			self.__backupUserManager = backupUserManager

			self.__sudoScriptRunner = sudoScriptRunner

			self.__systemAccountManager = SystemAccountManager(sudoScriptRunner)

			self.__ctx = _UploadSlotContext(backupUserManager, sudoScriptRunner, self.__systemAccountManager)

			log2.notice("Directory for persisting slot states: " + slotStatesDirPath)
			baseDir, finalDirName = os.path.split(slotStatesDirPath)
			self.__pm = jk_simpleobjpersistency.PersistencyManager2(baseDir)
			self.__pm.registerClass(
				clazz = UploadSlot,
				defaults = None,
				dirPath = finalDirName,
				autoStore = True,
				ctx = self.__ctx,
			)

			# --------------------------------

			self.__uploadSlots = {}					# str -> UploadSlot

			# get all IDs about persistent objects; we require these to later on delete objects we might no longer need;
			remainingObjectIDs = set(self.__pm.allIdentifiers(UploadSlot))
			#print(remainingObjectIDs)

			# now reconstruct all upload slot objects
			for systemAccount in self.__systemAccountManager.accounts:
				uploadSlotID = systemAccount.userName
				with log2.descend("Upload slot: " + uploadSlotID) as log3:
					uploadSlot = self.__pm.getObject(UploadSlot, uploadSlotID)
					if uploadSlot is None:
						log3.notice("Creating new upload slot object")
						uploadSlot = UploadSlot()
						uploadSlot.initialize(self.__ctx, systemAccount)
						self.__pm.addExternalObject(uploadSlot, uploadSlotID)
						uploadSlot.store()
					else:
						log3.notice("Reinstantiating existing upload slot object")

					if self.__fileSystemMountPoint != uploadSlot.fsMountPoint:
						raise Exception("Home directory not on this file system as expected: " + self.__fileSystemMountPoint)

					# verify various properties to ensure restricted access later
					dir_stats = os.stat(systemAccount.homeDir, follow_symlinks=False)
					if not stat.S_ISDIR(dir_stats.st_mode):
						raise Exception("Home directory of " + uploadSlotID + " is not a regular directory!")
					if dir_stats.st_uid != systemAccount.userID:
						raise Exception("Invalid user-ownership detected on home directory of " + uploadSlotID)
					if dir_stats.st_gid != systemAccount.groupID:
						raise Exception("Invalid group-ownership detected on home directory of " + uploadSlotID)

					# ensure restricted access
					currentDirMode = jk_utils.ChModValue(dir_stats.st_mode)
					expectedDirMode = jk_utils.ChModValue("rwx------")
					if str(currentDirMode) != str(expectedDirMode):
						raise Exception("Directory mode of home directory is '{}', not '{}' as expected!".format(
							str(currentDirMode),
							str(expectedDirMode)
						))
					log3.notice("Directory mode of home directory is '{}' as required.".format(
						str(currentDirMode)
					))

					# TODO: write a sudo script that sets ownership and access restrictions.
					# NOTE: we can't set the mode as we don't have the privileges; we are not running as superuser typically, but as 'thaniya'!
					#log3.notice("Restricting access to home directory to " + uploadSlotID + " only ...")
					#os.chmod(systemAccount.homeDir, jk_utils.ChModValue("rwx------").toInt())

					self.__uploadSlots[uploadSlotID] = uploadSlot
					log3.notice("Upload slot status: {}".format(str(uploadSlot.state)))

				if uploadSlotID in remainingObjectIDs:
					remainingObjectIDs.remove(uploadSlotID)

			# remove all objects that do no longer correspond to system accounts
			for objID in remainingObjectIDs:
				self.__pm.destroyObjectByID(objID)

			# ----

			self.__nSecuritySpaceMarginBytes = nSecuritySpaceMarginBytes
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def fsSecuritySpaceMarginBytes(self) -> int:
		return self.__nSecuritySpaceMarginBytes
	#

	#
	# Get the mount point of the file system all slots are using.
	#
	# NOTE: See the description of this class for important details!
	#
	@property
	def fsMountPoint(self) -> str:
		return self.__fileSystemMountPoint
	#

	@property
	def slots(self) -> typing.List[UploadSlot]:
		keys = sorted(self.__uploadSlots.keys())
		return [ self.__uploadSlots[key] for key in keys ]
	#

	@property
	def estimatedDiskSpaceRequired(self) -> int:
		self.__nSecuritySpaceMarginBytes
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	#
	# This method is called if a connection was idle for too long.
	#
	@jk_typing.checkFunctionSignature()
	def _onSlotTimeout(self, uploadSlot:UploadSlot, log:jk_logging.AbstractLogger):
		try:
			uploadSlot.timeout()
		except Exception as ee:
			log.error(ee)
	#

	@jk_typing.checkFunctionSignature()
	def _onSlotComplete(self, uploadSlot:UploadSlot, log:jk_logging.AbstractLogger):
		try:
			uploadSlot.completed()
		except Exception as ee:
			log.error(ee)
	#

	#
	# This method is called on timeout slots.
	#
	@jk_typing.checkFunctionSignature()
	def _onSlotAbort(self, uploadSlot:UploadSlot, log:jk_logging.AbstractLogger):
		try:
			uploadSlot.reset(log)
		except Exception as ee:
			log.error(ee)
	#

	#
	# This method is called if an upload succeeded and the client has disconnected.
	#
	@jk_typing.checkFunctionSignature()
	def _onSlotForward(self, uploadSlot:UploadSlot, log:jk_logging.AbstractLogger):
		try:
			with log.descend("Moving uploaded files to result directory ...") as log2:
				resultDirPath = uploadSlot.moveFilesToSpoolDirAndReset(log2)
				log2.notice("Directory with uploaded data: " + resultDirPath)
		except Exception as ee:
			log.error(ee)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def getSlot(self, uploadSlotID:str) -> typing.Union[UploadSlot,None]:
		return self.__uploadSlots.get(uploadSlotID)
	#

	def getSlotE(self, uploadSlotID:str) -> UploadSlot:
		ret = self.__uploadSlots.get(uploadSlotID)
		if ret is None:
			raise APIError("errNoSuchSlot")
		return ret
	#

	#
	# Invoke this method frequently - every 30 seconds or so - in order to detect and handle timeouts
	#
	def checkAndManageSlots(self, log:jk_logging.AbstractLogger):
		for uploadSlot in self.__uploadSlots.values():
			uploadSlot.updateUploadStateData()
			#print(uploadSlot.identifier, uploadSlot.state)

			if uploadSlot.state == EnumUploadSlotState.UNKNOWN:
				# reset the upload slots it in unknown states
				uploadSlot.reset(log)

			elif uploadSlot.state == EnumUploadSlotState.UPLOADING:
				# we're uploading; check if there is a timeout;
				if uploadSlot.lastUsedByClientTime is not None:
					dt = time.time() - uploadSlot.lastUsedByClientTime
				else:
					dt = time.time() - uploadSlot.allocationTime
				if dt > 5*60:											# 5 minutes				# TODO: make this configurable
					log.notice("Timeout at slot: {}".format(uploadSlot.identifier))
					self._onSlotTimeout(uploadSlot, log)

			elif uploadSlot.state == EnumUploadSlotState.FINALIZING:
				# the client has indicated success for the upload. let's wait for a disconnect.
				if not uploadSlot.isInUseByClientNoCaching:
					# no connection (any more)
					self._onSlotComplete(uploadSlot, log)
				else:
					# do nothing. wait.
					pass

			elif uploadSlot.state == EnumUploadSlotState.TIMEOUT:
				# a timeout occurred
				if uploadSlot.lastUsedByClientTime is not None:
					dt = time.time() - uploadSlot.lastUsedByClientTime
				else:
					dt = time.time() - uploadSlot.allocationTime
				if dt > 10*60:											# 10 minutes				# TODO: make this configurable
					log.notice("Resetting timeout state at slot: {}".format(uploadSlot.identifier))
					self._onSlotAbort(uploadSlot, log)

			elif uploadSlot.state == EnumUploadSlotState.COMPLETED:
				# the client completed the upload and has disconnect.
				log.notice("Processing successful upload in slot: {}".format(uploadSlot.identifier))
				self._onSlotForward(uploadSlot, log)
	#

	#
	# Allocate an upload slot
	#
	# NOTE: See the description of this class for important details!
	#
	# @return		dict jClientData		Either allocates an upload slot and returns a dictionary with data for the client or raises an APIError with "errNOFreeUploadSlot".
	#
	@jk_typing.checkFunctionSignature()
	def allocateSlot(self, backupUser:BackupUser, peerNetworkAddress:str, estimatedTotalBytesToUpload:typing.Union[int,None], log:jk_logging.AbstractLogger) -> dict:
		if estimatedTotalBytesToUpload is not None:
			fsStats = self.getFileSystemStats()
			nBytesRequired = int(estimatedTotalBytesToUpload * 1.1 + 64*1024*1024)
			#if nBytesRequired > 
		#

		ipAddressTriples = jk_utils.ip.getIPs()
		if not ipAddressTriples:
			raise Exception("Failed to detect local IP address!")
		localIPAddress = ipAddressTriples[0]
		localTCPPort = 22

		for uploadSlot in self.__uploadSlots.values():
			if uploadSlot.state == EnumUploadSlotState.READY:
				log.notice("Free upload slot found: {}".format(uploadSlot.identifier))
				ret = uploadSlot.allocate(backupUser, peerNetworkAddress, estimatedTotalBytesToUpload)
				ret["ipaddr"] = localIPAddress
				ret["port"] = localTCPPort
				return ret

		raise APIError("errNoFreeUploadSlot")
	#

	#
	# This method is called by the API if the client signalled via the API that he completed the upload.
	# Nevertheless the client my still be connected (and modify data after this method is invoked).
	#
	@jk_typing.checkFunctionSignature()
	def finalizingUpload(self, backupUser:BackupUser, uploadSlotID:str, log:jk_logging.AbstractLogger):
		# get slot

		uploadSlot = self.getSlotE(uploadSlotID)

		# verify that this user is allowed to modify this slot

		assert uploadSlot.backupUser is not None
		if uploadSlot.state != EnumUploadSlotState.UPLOADING:
			raise APIError("errInvSlotState")
		if uploadSlot.backupUser != backupUser:
			raise APIError("errArgs")

		# everything seems to be okay

		uploadSlot.finalizing()
	#

	@jk_typing.checkFunctionSignature()
	def resetSlot(self, backupUser:BackupUser, uploadSlotID:str, log:jk_logging.AbstractLogger):
		# get slot

		uploadSlot = self.getSlotE(uploadSlotID)

		# verify that this user is allowed to modify this slot

		if uploadSlot.state != EnumUploadSlotState.UPLOADING:
			raise APIError("errInvSlotState")
		assert uploadSlot.backupUser is not None
		if uploadSlot.backupUser != backupUser:
			raise APIError("errArgs")

		# everything seems to be okay

		uploadSlot.reset()
	#

	#
	# Retrieve information about the fill state of the file system.
	#
	# NOTE: See the description of this class for important details!
	#
	@jk_cachefunccalls.cacheCalls(seconds=5)
	def getFileSystemStats(self) -> jk_utils.fsutils.FileSystemStats:
		return jk_utils.fsutils.getFileSystemStats(self.__fileSystemMountPoint)
	#

#





















