


import typing

from .CfgKeyValueDefinition import CfgKeyValueDefinition






class AbstractCfgComponent(object):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, validKeys:typing.List[CfgKeyValueDefinition]):
		for v in validKeys:
			assert isinstance(v, CfgKeyValueDefinition)

		self.__validKeys = validKeys
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

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
			ret[keyDef.key] = getattr(self, "_" + keyDef.key)
		return ret
	#

	def loadFromJSON(self, jData:dict):
		assert isinstance(jData, dict)

		for keyDef in self.__validKeys:
			value = jData.get(keyDef.key)
			self.__verifyValueE(keyDef, value)
			setattr(self, "_" + keyDef.key, value)
	#

	def getValue(self, name:str):
		for keyDef in self.__validKeys:
			if keyDef.key == name:
				return getattr(self, "_" + name)
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

#








