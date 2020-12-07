


import typing
import re

import jk_typing

from .CfgKeyValueDefinition import CfgKeyValueDefinition
from .AbstractCfgComponent import AbstractCfgComponent





class CfgComponent_Magic(AbstractCfgComponent):

	__VALID_KEYS = [
		CfgKeyValueDefinition("magic", str, False),
		CfgKeyValueDefinition("version", int, False),
		CfgKeyValueDefinition("comment", int, True),
	]

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self):
		super().__init__(CfgComponent_Magic.__VALID_KEYS)

		self._comment = None

		self._magic = getattr(self, "MAGIC")		# str
		assert isinstance(self._magic, str)

		self._version = getattr(self, "VERSION")	# int
		assert isinstance(self._version, int)

		assert isinstance(getattr(self, "VALID_VERSIONS"), (list,tuple))		# list
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def validate(self):
		assert self._magic == getattr(self, "MAGIC")
		assert self._version in getattr(self, "VALID_VERSIONS")
	#

	def validateHighest(self):
		assert self._magic == getattr(self, "MAGIC")
		assert self._version in getattr(self, "VALID_VERSIONS")
		if self._version != getattr(self, "VERSION"):
			raise Exception("Version number encountered is not equal to highest version number as expected!")
	#

	def isValid(self) -> bool:
		if self._magic != getattr(self, "MAGIC"):
			return False
		if self._version not in getattr(self, "VALID_VERSIONS"):
			return False
		return True
	#

	def isValidHighest(self) -> int:
		if self._magic != getattr(self, "MAGIC"):
			return -1
		if self._version not in getattr(self, "VALID_VERSIONS"):
			return -1
		return self._version == getattr(self, "VERSION")
	#

#










