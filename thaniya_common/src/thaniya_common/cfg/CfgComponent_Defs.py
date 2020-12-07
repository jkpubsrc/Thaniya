


import typing
import re

import jk_prettyprintobj

from .CfgKeyValueDefinition import CfgKeyValueDefinition






class CfgComponent_Defs(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self):
		self.__definitions = {}
		self.__replacements = {}				# forward resolution of variables
		self.__replacementsReverse = {}			# backward resolution of variable
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dump(self, ctx:jk_prettyprintobj.DumpCtx):
		ctx.dumpVar("definitions", self.__definitions)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def loadFromJSON(self, jData:dict):
		assert isinstance(jData, dict)

		for key, value in jData.items():
			assert isinstance(key, str)
			assert re.fullmatch("[A-Z][A-Z_]*", key)
			assert isinstance(value, str)

		self.__definitions = jData

		self.__replacements = {
			"$(" + key + ")":value for key, value in jData.items()
		}
		self.__replacementsReverse = {
			value:key for key, value in self.__replacements.items()
		}
	#

	def resolveValue(self, text:str) -> str:
		for key, value in self.__replacements.items():
			text = text.replace(key, value)
		m = re.match("\$\(([a-zA-Z_]+)\)", text)
		if m:
			raise Exception("Invalid variable: " + repr(m.group(1)))
		return text
	#

	def simplifyValue(self, text:str) -> str:
		for key, value in self.__replacementsReverse.items():
			text = text.replace(key, value)
		return text
	#

	def toJSON(self) -> dict:
		return self.__definitions
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#








