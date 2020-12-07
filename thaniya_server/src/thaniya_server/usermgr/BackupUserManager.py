


import os

import jk_simpleobjpersistency
import jk_typing
import jk_logging

from ..utils.APIError import APIError
from .BackupUser import BackupUser







class BackupUserManager(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# NOTE: If this object is set to readonly this does not prevent individual objects to be stored. It just prevents the user manager
	# from creating/deleting users.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, usersDirPath:str, bReadWrite:bool, log:jk_logging.AbstractLogger):
		if not os.path.isdir(usersDirPath):
			raise Exception("No such directory: " + usersDirPath)

		self.__bIsReadOnly = not bReadWrite
		if self.__bIsReadOnly:
			log.notice("User manager is initialized in read only mode.")
		else:
			log.notice("User manager is initialized in read-write mode.")

		baseDir, finalDirName = os.path.split(usersDirPath)
		self.__pm = jk_simpleobjpersistency.PersistencyManager2(baseDir)
		self.__pm.registerClass(BackupUser, None, finalDirName, True)

		self.__privilegeDefaults = {
			"privChangeOwnLoginPwd": True,
			"privChangeOwnBackupUploadPwd": True,
		}

		self.reloadUsers()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def users(self) -> list:
		ret = []
		for u in self.__pm.getAllObjectsAsList(BackupUser):
			u._userMgr = self
			ret.append(u)
		return ret
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def hasPrivilege(self, user:BackupUser, privilegeName:str) -> bool:
		if privilegeName not in self.__privilegeDefaults:
			# no such privilege -> reject
			return False
		return self.__privilegeDefaults[privilegeName]
	#

	#
	# Returns a set of user names the specified user may have access to. This includes the supervised users.
	#
	def getAccessableUserNames(self, user:BackupUser) -> set:
		limitToUsers = set([ user.userName ])

		# TODO: move thie correction code to the loading facility

		validSupervisedUsers = []
		bNeedUpdate = False
		for otherUserName in user.supervises:
			u = self.getUser(otherUserName)
			if u:
				# we found this user -> this is good
				validSupervisedUsers.append(otherUserName)
				limitToUsers.add(otherUserName)
			else:
				bNeedUpdate = True

		if user.userName in validSupervisedUsers:
			validSupervisedUsers.remove(user.userName)
			bNeedUpdate = True

		if not self.__bIsReadOnly:
			if bNeedUpdate:
				user.supervises = validSupervisedUsers
				user.store()

		return limitToUsers
	#

	def reloadUsers(self):
		self.__pm.clearClassCache(BackupUser)
		self.__pm.loadAllObjects(BackupUser)
	#

	# ----------------------------------------------------------------

	def createUser(self, userName:str, passwordHash:str, eMail:str, role:str, comment:str = None, enabled:bool = True) -> BackupUser:
		if self.__bIsReadOnly:
			raise Exception("Read only!")

		assert isinstance(userName, str)

		if self.__pm.objectExists(BackupUser, userName):
			raise APIError("errUserExists", "User already exists: " + repr(userName))

		obj = self.__pm.createObject(BackupUser, userName)
		obj.userName = userName
		obj.passwordHash = passwordHash
		obj.eMail = eMail
		obj.role = role
		obj.comment = comment
		obj.enabled = enabled
		#obj.is_authenticated = True

		obj.store()

		obj._userMgr = self
		return obj
	#

	def deleteUser(self, userName:str):
		if self.__bIsReadOnly:
			raise Exception("Read only!")

		assert isinstance(userName, str)

		if self.__pm.objectExists(BackupUser, userName):
			self.__pm.destroyObjectByID(BackupUser, userName)
		else:
			raise Exception("no such user: " + repr(userName))
	#

	def getUser(self, userName:str) -> BackupUser:
		assert isinstance(userName, str)

		ret = self.__pm.getObject(BackupUser, userName)
		if ret is not None:
			ret._userMgr = self
		return ret
	#

	def getUserE(self, userName:str) -> BackupUser:
		assert isinstance(userName, str)

		ret = self.__pm.getObject(BackupUser, userName)
		if ret is None:
			raise APIError("errNoSuchUser", "No such user: " + repr(userName))
		ret._userMgr = self
		return ret
	#

	"""
	def getBackupUserBySessionID(self, sessionID:str) -> BackupUser:
		assert isinstance(sessionID, str)

		for user in self.__pm.getAllObjectsAsList(BackupUser):
			assert isinstance(user, BackupUser)
			if user.backup_sessionID == sessionID:
				user._userMgr = self
				return user

		return None
	#
	"""

	def countUsers(self) -> int:
		return self.__pm.countObjects(BackupUser)
	#

	# ----------------------------------------------------------------

	"""
	def createDiskSpaceReservation(self, accountName:str) -> jk_uploadshares.DiskSpaceReservation:
		assert isinstance(accountName, str)

		if accountName in self.__diskSpaceReservations:
			raise Exception("A disk space reservation already exists for: " + repr(accountName))
		obj = self.__pm.createObject(jk_uploadshares.DiskSpaceReservation, accountName)
		obj.store()
		self.__diskSpaceReservations[accountName] = obj

		obj._userMgr = self
		return obj
	#

	def getDiskSpaceReservation(self, accountName:str) -> jk_uploadshares.DiskSpaceReservation:
		assert isinstance(accountName, str)

		return self.__diskSpaceReservations[accountName]
	#

	def addDiskSpaceReservation(self, r:jk_uploadshares.DiskSpaceReservation):
		assert isinstance(r, jk_uploadshares.DiskSpaceReservation)

		if r.accountName in self.__diskSpaceReservations:
			raise Exception("A disk space reservation already exists for: " + repr(r.accountName))
		self.__pm.addExternalObject(r, r.accountName)
	#

	@property
	def diskSpaceReservations(self) -> list:
		return list(self.__diskSpaceReservations.values())
	#
	"""

	# ----------------------------------------------------------------

#






