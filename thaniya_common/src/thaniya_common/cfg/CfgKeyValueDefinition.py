



import collections

import jk_prettyprintobj





class CfgKeyValueDefinition(jk_prettyprintobj.DumpMixin):

	__slots__ = (
		"key",
		"pyType",
		"nullable",
		"parserFunc",
		"toJSONFunc",
		"defaultValue",
	)

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	#
	# @param		str key					(required) The name of the key in the section of a configuration file
	# @param		str pyType				(required) The python type (not: tuple of types!) a key value must be of
	# @param		callable parserFunc		(optional) A function that performs parsing of stored JSON data (prior to validation of the key value).
	# @param		callable toJSONFunc		(optional) A function that creates JSON data on write.
	#
	def __init__(self, key:str, pyType:type, nullable:bool, parserFunc = None, toJSONFunc = None, defaultValue = None):
		assert isinstance(key, str)
		assert type(pyType) == type
		assert isinstance(nullable, bool)
		if parserFunc is not None:
			assert callable(parserFunc)
		if toJSONFunc is not None:
			assert callable(toJSONFunc)

		self.key = key
		self.pyType = pyType
		self.nullable = nullable
		self.parserFunc = parserFunc
		self.toJSONFunc = toJSONFunc
		self.defaultValue = defaultValue
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"key",
			"pyType",
			"nullable",
			"parserFunc",
			"toJSONFunc",
			"defaultValue",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#







