


import json

import jk_json
import jk_typing

from .cfg.CfgKeyValueDefinition import CfgKeyValueDefinition
from .cfg.AbstractCfgComponent import AbstractCfgComponent








class _Magic(AbstractCfgComponent):

	MAGIC = "thaniya-client-stats"

	__VALID_KEYS = [
		CfgKeyValueDefinition("magic", str, False),
		CfgKeyValueDefinition("version", int, False),
	]

	def __init__(self):
		super().__init__(_Magic.__VALID_KEYS)

		self._magic = _Magic.MAGIC				# str
		self._version = 1						# int
	#

#



class _DataV1(AbstractCfgComponent):

	__VALID_KEYS = [
		CfgKeyValueDefinition("tStart",					float,		True),
		CfgKeyValueDefinition("tEnd",					float,		True),
		CfgKeyValueDefinition("bSuccess",				bool,		True),
		CfgKeyValueDefinition("expectedBytesToWrite",	int,		True),
		CfgKeyValueDefinition("totalBytesWritten",		int,		True),
		CfgKeyValueDefinition("avgWritingSpeed",		float,		True),
		CfgKeyValueDefinition("simulate",				bool,		True),
		CfgKeyValueDefinition("d0_calcDiskSpace",		float,		True),
		CfgKeyValueDefinition("d1_connectAndPrepare",	float,		True),
		CfgKeyValueDefinition("d2_backup",				float,		True),
		CfgKeyValueDefinition("hostName",				str,		True),
		CfgKeyValueDefinition("backupUserName",			str,		True),
		CfgKeyValueDefinition("backupIdentifier",		str,		True),
	]

	def __init__(self):
		super().__init__(_DataV1.__VALID_KEYS)

		self._tStart = None						# float
		self._tEnd = None						# float
		self._bSuccess = None					# bool
		self._expectedBytesToWrite = None		# int
		self._totalBytesWritten = None			# int
		self._avgWritingSpeed = None			# float
		self._simulate = None					# bool
		self._d0_calcDiskSpace = None			# float
		self._d1_connectAndPrepare = None		# float
		self._d2_backup = None					# float
		self._hostName = None					# str
		self._backupUserName = None				# str					# the user that performed the backup (not: the user the backup is performed for)
		self._backupIdentifier = None			# str
	#

#



#
# Represents status and statistical information about a backup performed.
#
class ThaniyaBackupStats(object):

	__slots__ = (
		"_magic",
		"_data",
	)

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self):
		self._magic = _Magic()
		self._data = _DataV1()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def writeToFile(self, filePath:str):
		assert isinstance(filePath, str)

		jk_json.saveToFilePretty(self.toJSON(), filePath)
	#

	def toJSON(self) -> dict:
		ret = {
			"magic": self._magic.toJSON(),
			"data": self._data.toJSON(),
		}
		return ret
	#

	def __str__(self):
		return json.dumps(self.toJSON(), indent="\t", sort_keys=True)
	#

	@staticmethod
	def loadFromFile(filePath:str):
		assert isinstance(filePath, str)
		jData = jk_json.loadFromFile(filePath)

		return ThaniyaBackupStats.loadFromJSON(jData)
	#

	@staticmethod
	def loadFromJSON(jData:dict):
		assert isinstance(jData, dict)

		ret = ThaniyaBackupStats()

		ret._magic.loadFromJSON(jData["magic"])
		assert ret._magic._magic == _Magic.MAGIC
		assert ret._magic._version == 1

		ret._data.loadFromJSON(jData["data"])

		return ret
	#

	#
	# Use this method to set a data value.
	#
	@jk_typing.checkFunctionSignature()
	def setValue(self, name:str, value):
		self._data.setValue(name, value)
	#

	#
	# Use this method to read a data value.
	#
	@jk_typing.checkFunctionSignature()
	def getValue(self, name:str):
		return self._data.getValue(name)
	#

#









