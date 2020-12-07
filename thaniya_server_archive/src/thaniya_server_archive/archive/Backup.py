

import typing
import re
import time
import os
import random
import datetime

import jk_utils
import jk_json
import jk_typing

from .ArchivedBackupInfoFile import ArchivedBackupInfoFile
from .BackupDataFile import BackupDataFile








def _toInt(s:str) -> int:
	while (len(s) > 1) and s[0] == "0":
		s = s[1:]
	return int(s)
#



#
# This class represents a backup within the archive.
#
class Backup(object):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, dirPath:str):
		self.__dirPath = dirPath
		self.__infoFile = ArchivedBackupInfoFile.loadFromFile(os.path.join(dirPath, "_backup_info.json"))

		self.__files = []
		for fe in os.scandir(dirPath):
			if bool(re.match("[a-zA-Z0-9]", fe.name[0])) and fe.is_file():
				self.__files.append(BackupDataFile(fe))

		self.__files = tuple(self.__files)

		self.__cached_dtBackupStart = None
		self.__cached_sBackupStartDate = None
		self.__cached_sBackupStartDateTime = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def files(self) -> typing.Tuple[BackupDataFile]:
		return self.__files
	#

	@property
	def dirPath(self) -> str:
		return self.__dirPath
	#

	@property
	def dtBackupStart(self) -> datetime.datetime:
		if self.__cached_dtBackupStart is None:
			#self.__cached_dtBackupStart = datetime.datetime.fromtimestamp(self.__infoFile.getValue("tBackupStart"))
			self.__cached_dtBackupStart = self.__infoFile.getValue("tBackupStart").dateTime
		return self.__cached_dtBackupStart
	#

	#
	# Returns a human readable representation of the start time stamp in the form:
	# "YYYY-MM-DD"
	#
	@property
	def sBackupStartDate(self) -> str:
		dt = self.dtBackupStart
		if self.__cached_sBackupStartDate is None:
			self.__cached_sBackupStartDate = "{:04d}-{:02d}-{:02d}".format(
				dt.year,
				dt.month,
				dt.day,
			)
		return self.__cached_sBackupStartDate
	#

	#
	# Returns a human readable representation of the start time stamp in the form:
	# "YYYY-MM-DD hh:mm:ss"
	#
	@property
	def sBackupStartDateTime(self) -> str:
		dt = self.dtBackupStart
		if self.__cached_sBackupStartDateTime is None:
			self.__cached_sBackupStartDateTime = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
				dt.year,
				dt.month,
				dt.day,
				dt.hour,
				dt.minute,
				dt.second,
			)
		return self.__cached_sBackupStartDateTime
	#

	#
	# Returns a machine readable representation of the start time stamp in the form:
	# {
	#		"year": ...,
	#		"month": ...,
	#		"day": ...,
	#		"hour": ...,
	#		"minute": ...,
	#		"second": ...,
	# }
	#
	@property
	def jBackupStartDateTime(self) -> dict:
		dt = self.dtBackupStart
		return {
			"year": dt.year,
			"month": dt.month,
			"day": dt.day,
			"hour": dt.hour,
			"minute": dt.minute,
			"second": dt.second,
		}
	#

	#
	# Returns a machine readable representation of the start time stamp in the form:
	# ( ..year.., ..month.., ..day.., ..hour.., ..minute.., ..second.. )
	#
	@property
	def lBackupStartDateTime(self) -> tuple:
		dt = self.dtBackupStart
		return (
			dt.year,
			dt.month,
			dt.day,
			dt.hour,
			dt.minute,
			dt.second,
		)
	#

	@property
	def lBackupStartDate(self) -> tuple:
		dt = self.dtBackupStart
		return (
			dt.year,
			dt.month,
			dt.day,
		)
	#

	@property
	def timeStamp(self) -> jk_utils.TimeStamp:
		return self.__infoFile.getValue("tBackupStart")
	#

	@property
	def sizeInBytesUploaded(self) -> jk_utils.AmountOfBytes:
		return self.__infoFile.getValue("nTotalBytesUploaded")
	#

	@property
	def sizeInBytesArchived(self) -> jk_utils.AmountOfBytes:
		return self.__infoFile.getValue("nTotalBytesArchived")
	#

	@property
	def clientBackupDuration(self) -> float:
		return self.__infoFile.getValue("dClientBackupDuration")
	#

	@property
	def systemName(self) -> str:
		return self.__infoFile.getValue("systemName")
	#

	@property
	def backupUserName(self) -> str:
		return self.__infoFile.getValue("backupUserName")
	#

	@property
	def backupIdentifier(self) -> str:
		return self.__infoFile.getValue("backupIdentifier")
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	#
	# TODO: maybe move this to ArchiveDataStore? or a separate class?
	#
	@staticmethod
	@jk_typing.checkFunctionSignature()
	def buildRecommendedDirName(dt:datetime.datetime = None, systemName:str = None, backupUserName:str = None, backupIdentifier:str = None, backup = None) -> str:
		if backup is not None:
			assert isinstance(backup, Backup)
			dt = backup.dtBackupStart
			systemName = backup.systemName
			backupUserName = backup.backupUserName
			backupIdentifier = backup.backupIdentifier

		assert dt is not None
		Backup.verifySystemName(systemName)
		Backup.verifyBackupUserName(backupUserName)
		Backup.verifyBackupIdentifier(backupIdentifier)

		return "{}---{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}---{}---{}".format(
			systemName,
			dt.year,
			dt.month,
			dt.day,
			dt.hour,
			dt.minute,
			dt.second,
			backupUserName,
			backupIdentifier)
	#

	#
	# TODO: maybe move this to ArchiveDataStore? or a separate class?
	#
	@staticmethod
	def tryParseDirName(dirName:str) -> dict:
		m = re.match(r"^([a-zA-Z_\.0-9-\+%]+)---(\d\d\d\d)(\d\d)(\d\d)(\d\d)(\d\d)(\d\d)---([a-zA-Z_\.0-9-\+%]+)---([a-zA-Z_\.0-9-\+%]+)$", dirName)
		if m:
			return {
				"systemName": m.group(1),
				"year": _toInt(m.group(2)),
				"month": _toInt(m.group(3)),
				"day": _toInt(m.group(4)),
				"hour": _toInt(m.group(5)),
				"minute": _toInt(m.group(6)),
				"second": _toInt(m.group(7)),
				"userName": m.group(8),
				"backupIdentifier": m.group(9),
			}
		return None
	#

	#
	# TODO: maybe move this to ArchiveDataStore? or a separate class?
	#
	@staticmethod
	def verifySystemName(systemName:str):
		assert re.match(r".*(---|\.\.|\s).*", systemName) is None
		assert re.match(r"^[a-zA-Z_\.0-9-\+%]+$", systemName) is not None
	#

	#
	# TODO: maybe move this to ArchiveDataStore? or a separate class?
	#
	@staticmethod
	def verifyBackupUserName(userName:str):
		assert re.match(r".*(---|\.\.|\s).*", userName) is None
		assert re.match(r"^[a-zA-Z_\.0-9-\+%]+$", userName) is not None
	#

	#
	# TODO: maybe move this to ArchiveDataStore? or a separate class?
	#
	@staticmethod
	def verifyBackupIdentifier(backupIdentifier:str):
		assert re.match(r".*(---|\.\.|\s).*", backupIdentifier) is None
		assert re.match(r"^[a-zA-Z_\.0-9-\+%]+$", backupIdentifier) is not None
	#

#















