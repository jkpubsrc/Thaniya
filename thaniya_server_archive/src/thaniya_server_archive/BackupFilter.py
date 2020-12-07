



import typing

from .archive.Backup import Backup







#
# This class implements filtering for backups.
#
class BackupFilter(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self,
				systemName:str = None,
				backupUserName:str = None,
				backupUserNames:typing.List[str] = None,
				backupIdentifier:str = None,
				year:int = None,
				month:int = None,
				day:int = None
			):

		self.systemName = systemName

		if backupUserName:
			self.backupUserNames = [ backupUserName ]
		else:
			self.backupUserNames = None
			if backupUserNames is not None:
				assert isinstance(backupUserNames, (set,tuple,list))
				self.backupUserNames = set(backupUserNames)

		self.backupIdentifier = backupIdentifier

		self.year = year

		self.month = month

		self.day = day
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

	def cloneObject(self):
		return BackupFilter(
			systemName = self.systemName,
			backupUserNames = None if self.backupUserNames is None else set(self.backupUserNames),
			year = self.year,
			month = self.month,
			day = self.day,
		)
	#

	def restrictToUserNames(self, userNameSet:set):
		b = self.cloneObject()
		if b.backupUserNames is None:
			b.backupUserNames = set(userNameSet)
		else:
			b.backupUserNames = userNameSet.intersection(b.backupUserNames)
		return b
	#

	def isMatch(self, backup:Backup) -> bool:
		if self.systemName is not None:
			if backup.systemName != self.systemName:
				return False

		if self.backupUserNames is not None:
			if backup.backupUserName not in self.backupUserNames:
				return False

		if self.backupIdentifier is not None:
			if backup.backupIdentifier != self.backupIdentifier:
				return False

		dtBackupStart = backup.dtBackupStart
		if self.year is not None:
			if dtBackupStart.year != self.year:
				return False

		if self.month is not None:
			if dtBackupStart.month != self.month:
				return False

		if self.day is not None:
			if dtBackupStart.day != self.day:
				return False

		return True
	#

#


















