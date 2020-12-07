


import typing
import json

import jk_typing
import jk_json
import jk_prettyprintobj

from .AbstractCfgComponent import AbstractCfgComponent
from .CfgComponent_Defs import CfgComponent_Defs
from .CfgComponent_Magic import CfgComponent_Magic








class AbstractAppCfg(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self, compMagicType:type, bWithDefs:bool, groups:dict):
		assert isinstance(compMagicType, type)

		assert isinstance(bWithDefs, bool)

		assert isinstance(groups, dict)
		for k, v in groups.items():
			assert isinstance(k, str)
			assert isinstance(v, AbstractCfgComponent)

		self._magic = compMagicType()

		if bWithDefs:
			self._defs = CfgComponent_Defs()
			for v in groups.values():
				v._varResolver = self._defs
		else:
			self._defs = None

		self._groups = groups
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		if self._defs:
			return [
				"_magic",
				"_defs",
				"_groups",
			]
		else:
			return [
				"_magic",
				"_groups",
			]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def writeToFile(self, filePath:str):
		assert isinstance(filePath, str)

		jk_json.saveToFilePretty(self.toJSON(), filePath)
	#

	def toJSON(self) -> dict:
		ret = {
			"magic": self._magic.toJSON(),
		}

		if self._defs:
			ret["defs"] = self._defs.toJSON()

		for groupName, group in self._groups.items():
			ret[groupName] = group.toJSON()
		return ret
	#

	def __str__(self):
		return json.dumps(self.toJSON(), indent="\t", sort_keys=True)
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
		return group.getValue(varName)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _loadFromJSON(self, jData:dict):
		assert isinstance(jData, dict)

		self._magic.loadFromJSON(jData["magic"])
		self._magic.validateHighest()

		if self._defs:
			self._defs.loadFromJSON(jData["defs"])

		for groupName, group in self._groups.items():
			if groupName in jData:
				group.loadFromJSON(jData[groupName])
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#










