


import typing
import re

import jk_prettyprintobj

from .CfgComponent_Defs import CfgComponent_Defs
from .CfgKeyValueDefinition import CfgKeyValueDefinition






class AbstractCfgComponent(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, validKeys:typing.List[CfgKeyValueDefinition] = None, varResolver:CfgComponent_Defs = None):
		if validKeys is None:
			validKeys = getattr(self, "VALID_KEYS")
		assert isinstance(validKeys, (list,tuple))
		for v in validKeys:
			assert isinstance(v, CfgKeyValueDefinition)
		self.__validKeys = validKeys

		if varResolver is not None:
			assert isinstance(varResolver, CfgComponent_Defs)
		self._varResolver = varResolver
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dump(self, ctx:jk_prettyprintobj.DumpCtx):
		for keyDef in self.__validKeys:
			#ctx.dumpVar("_" + keyDef.key, getattr(self, "_" + keyDef.key))
			ctx.dumpVar(keyDef.key, self.getValue(keyDef.key))
	#

	def __verifyValueE(self, keyDef:CfgKeyValueDefinition, value):
		if value is None:
			if not keyDef.nullable:
				raise Exception("Value for {} must not be null!".format(keyDef.key))
		else:
			if keyDef.pyType is not None:
				# we have a type definition (which we should have!)
				if not isinstance(value, keyDef.pyType):
					raise Exception("Value is not of type '{}'!".format(str(keyDef.pyType.__name__)))
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __getitem__(self, name:str):
		return self.getValue(name)
	#

	def __setitem__(self, name:str, value):
		return self.setValue(name, value)
	#

	def toJSON(self) -> dict:
		ret = {}
		for keyDef in self.__validKeys:
			v = getattr(self, "_" + keyDef.key)
			if (v is not None) and keyDef.toJSONFunc:
				v = keyDef.toJSONFunc(v)
			ret[keyDef.key] = self._varResolver.simplifyValue(v) if self._varResolver and isinstance(v, str) else v
		return ret
	#

	def loadFromJSON(self, jData:dict):
		assert isinstance(jData, dict)

		for keyDef in self.__validKeys:
			value = jData.get(keyDef.key)
			if (value is not None) and keyDef.parserFunc:
				value = keyDef.parserFunc(value)
				assert value is not None

			if self._varResolver and isinstance(value, str):
				value = self._varResolver.resolveValue(value)
			self.__verifyValueE(keyDef, value)
			#print("setattr(self, \"_\" + " + keyDef.key + ", " + str(value) + ")", "=>", self)
			setattr(self, "_" + keyDef.key, value)
	#

	def getValue(self, name:str):
		for keyDef in self.__validKeys:
			if keyDef.key == name:
				v = getattr(self, "_" + name)
				if v is None:
					return keyDef.defaultValue
				return v
		raise Exception("Invalid property name: " + repr(name))
	#

	def setValue(self, name:str, value):
		for keyDef in self.__validKeys:
			if keyDef.key == name:
				# KVP found!
				self.__verifyValueE(keyDef, value)
				setattr(self, "_" + name, value)
				return
		raise Exception("Invalid property name: " + repr(name))
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#








