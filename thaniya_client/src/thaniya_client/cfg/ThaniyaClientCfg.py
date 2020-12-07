

import os
import json

import jk_json
import jk_utils
import jk_typing
import jk_logging

from .CfgKeyValueDefinition import CfgKeyValueDefinition
from .AbstractCfgComponent import AbstractCfgComponent








class _Magic(AbstractCfgComponent):

	MAGIC = "thaniya-client-cfg"

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



class _GeneralV1(AbstractCfgComponent):

	__VALID_KEYS = [
		CfgKeyValueDefinition("tempBaseDir",				str,		True),
	]

	def __init__(self):
		super().__init__(_GeneralV1.__VALID_KEYS)

		self._tempDir = None					# str
	#

#



#
# Represents status and statistical information about a backup performed.
#
class ThaniyaClientCfg(object):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self):
		self._magic = _Magic()
		self._groups = {
			"general": _GeneralV1()
		}
		self._parent = None					# a nested ThaniyaClientCfg or None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def general(self) -> AbstractCfgComponent:
		return self._groups["general"]
	#

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
		}
		for groupName, group in self._groups.items():
			ret[groupName] = group.toJSON()
		return ret
	#

	def __str__(self):
		return json.dumps(self.toJSON(), indent="\t", sort_keys=True)
	#

	@staticmethod
	def load(log:jk_logging.AbstractLogger = None):
		candidates = [
			"/etc/thaniya/client/configuration.jsonc",
			os.path.join(jk_utils.users.getUserHome(), ".config", "thaniya", "configuration.jsonc"),
		]

		cfgCurrent = None

		for c in candidates:
			if not os.path.isfile(c):
				continue
			log.notice("Loading configuration from file: " + c)
			cfgNext = ThaniyaClientCfg._loadFromFile(c)
			if cfgNext is not None:
				cfgNext._parent = cfgCurrent
				cfgCurrent = cfgNext

		return cfgCurrent
	#

	@staticmethod
	def _loadFromFile(filePath:str):
		assert isinstance(filePath, str)
		jData = jk_json.loadFromFile(filePath)

		return ThaniyaClientCfg._loadFromJSON(jData)
	#

	@staticmethod
	def _loadFromJSON(jData:dict):
		assert isinstance(jData, dict)

		ret = ThaniyaClientCfg()

		ret._magic.loadFromJSON(jData["magic"])
		assert ret._magic._magic == _Magic.MAGIC
		assert ret._magic._version == 1

		for groupName, group in ret._groups.items():
			if groupName in jData:
				group.loadFromJSON(jData[groupName])

		return ret
	#

	#
	# Use this method to set a data value.
	#
	@jk_typing.checkFunctionSignature()
	def setValue(self, groupName:str, varName:str, value):
		group = self._groups.get(groupName)
		if group is None:
			raise Exception("Invalid group: {}".format(groupName))
		group.setValue(varName, value)
	#

	#
	# Use this method to read a data value.
	#
	@jk_typing.checkFunctionSignature()
	def getValue(self, groupName:str, varName:str):
		group = self._groups.get(groupName)
		if group is None:
			raise Exception("Invalid group: {}".format(groupName))

		v = group.getValue(varName)

		if v is not None:
			return v

		if self._parent is not None:
			return self._parent.getValue(groupName, varName)
		return None
	#

#









