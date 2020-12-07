

import typing
import datetime
import socket

import jk_utils





#
# Provide various information about the origin of a backup.
# An instance of this class is used to feed information into various strategy implementations, such as the target directory strategies.
#
class ILocalBackupOriginInfo:

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# Time stamp of the start of this backup.
	#
	@property
	def backupDateTime(self) -> datetime.datetime:
		raise NotImplementedError()
	#

	#
	# Time stamp of the start of this backup in seconds since Epoch.
	#
	@property
	def backupEpochTime(self) -> int:
		raise NotImplementedError()
	#		

	#
	# The current host name we currently run this backup on.
	#
	@property
	def localHostName(self) -> str:
		raise NotImplementedError()
	#

	#
	# The current user performing this backup.
	#
	@property
	def currentUserName(self) -> str:
		raise NotImplementedError()
	#

	#
	# A string that identifies the type of backup. (There might be a variety of independent backups from different hosts.)
	#
	@property
	def backupIdentifier(self) -> typing.Union[None,str]:
		raise NotImplementedError()
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#












