


import json

import jk_json
import jk_typing
import jk_prettyprintobj

from jk_utils import AmountOfBytes
from jk_utils import TimeStamp

from thaniya_common.cfg import CfgKeyValueDefinition
from thaniya_common.cfg import AbstractCfgComponent
from thaniya_common.cfg import CfgComponent_Magic
from thaniya_common.cfg import AbstractAppCfg








class _DataV1(AbstractCfgComponent):

	__VALID_KEYS = [
		# NOTE: Convetion: all data provided by clients that might be untrue are marked with "Client"

		CfgKeyValueDefinition("tBackupStart",			TimeStamp,		True,	TimeStamp.parse,		float	),	# This is the time stamp the client invoked "allocate()"
		CfgKeyValueDefinition("tBackupEnd",				TimeStamp,		True,	TimeStamp.parse,		float	),	# This is the time stamp the client invoked "finalize()"
		CfgKeyValueDefinition("sizeInBytes",			AmountOfBytes,	True,	AmountOfBytes.parse,	int		),	# This is the total number of bytes for this backup (including meta files) as measured by the server
		CfgKeyValueDefinition("dClientBackupDuration",	float,			True									),	# This is the duration of the backup as told by the client.
		CfgKeyValueDefinition("systemName",				str,			True									),	# This is the official host name of the system a backup has been created for.
		CfgKeyValueDefinition("backupUserName",			str,			True									),	# This is the user name the client authenticated with.
		CfgKeyValueDefinition("backupIdentifier",		str,			True									),	# This is the identifier the client provided to associate the backup with
	]

	def __init__(self):
		super().__init__(_DataV1.__VALID_KEYS)

		self._tBackupStart = None				# TimeStamp
		self._tBackupEnd = None					# TimeStamp
		self._sizeInBytes = None				# AmountOfBytes
		self._dClientBackupDuration = None		# float
		self._systemName = None					# str
		self._backupUserName = None				# str
		self._backupIdentifier = None			# str
	#

#



class _Magic(CfgComponent_Magic):

	MAGIC = "thaniya-uploaded-backup-info"
	VERSION = 1
	VALID_VERSIONS = [ 1 ]

#






#
# Represents the contents of a backup information file that describes an upload file set.
#
class UploadedBackupInfoFile(AbstractAppCfg):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self):
		super().__init__(
			_Magic,
			False,
			{
				"data": _DataV1(),
			}
		)
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
	# Use this method to set a data value.
	#
	@jk_typing.checkFunctionSignature()
	def setValue(self, name:str, value):
		self._groups["data"].setValue(name, value)
	#

	#
	# Use this method to read a data value.
	#
	@jk_typing.checkFunctionSignature()
	def getValue(self, name:str):
		return self._groups["data"].getValue(name)
	#

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	@staticmethod
	def loadFromFile(filePath:str):
		assert isinstance(filePath, str)
		jData = jk_json.loadFromFile(filePath)

		return UploadedBackupInfoFile.loadFromJSON(jData)
	#

	@staticmethod
	def loadFromFile(filePath:str):
		assert isinstance(filePath, str)

		jData = jk_json.loadFromFile(filePath)

		ret = UploadedBackupInfoFile()
		ret._loadFromJSON(jData)

		return ret
	#

	@staticmethod
	def loadFromJSON(jData:dict):
		assert isinstance(jData, dict)

		ret = UploadedBackupInfoFile()
		ret._loadFromJSON(jData)

		return ret
	#

#









