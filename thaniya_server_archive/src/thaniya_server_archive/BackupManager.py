



import os
import typing

import jk_typing
import jk_utils
import jk_logging
import jk_json
import jk_prettyprintobj

from thaniya_server.usermgr import BackupUser

# do not include AppRuntimeArchiveHttpd here because otherwise we would have cyclic module references
from .archive import Backup, ArchiveDataStoreBase
from .BackupFilter import BackupFilter






#
# This class is some kind of facade to the archives. It's a gate keeper. Use an instance of this class to access the backups.
#
class BackupManager(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, appRuntime):
		# we can't check the type directly because we would have cyclic module references
		assert appRuntime.__class__.__name__ == "AppRuntimeArchiveHttpd"

		self.__appRuntime = appRuntime
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# @param		BackupUser actingUser			The user that performs the request.
	#												(Do not specify an exact type for python type verification here as we might
	#												get a proxy instead of the real user object.)
	#
	@jk_typing.checkFunctionSignature()
	def getBackups(self,
			actingUser,		# do not specify a type here as we might get a proxy instead of the real user object
			backupFilter:BackupFilter = None,
		) -> typing.List[Backup]:

		# build the user name filter

		limitToUsers = self.__appRuntime.userMgr.getAccessableUserNames(actingUser)

		# build filter

		if backupFilter is None:
			backupFilter = BackupFilter()
		backupFilter = backupFilter.restrictToUserNames(limitToUsers)

		# retrieve all backups and filter them

		backups = []
		for a in self.__appRuntime.archiveMgr.archives:
			assert isinstance(a, ArchiveDataStoreBase)
			for backup in a.backups:
				if backupFilter.isMatch(backup):
					# only accept backups the user has sufficient rights to see them
					backups.append(backup)

		# sort them

		backups = sorted(backups, key=lambda x: x.lBackupStartDateTime)

		# return them

		return backups
	#

#







