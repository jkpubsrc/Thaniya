


import typing
import re

import jk_typing





class FileNamePattern(object):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, pattern:str):
		parts = pattern.split("*")
		if len(parts) > 2:
			raise Exception("Invalid pattern: " + repr(pattern))

		compiledParts = [ "^" ]

		if len(parts) == 1:
			compiledParts.extend(self.__compilePart(parts[0]))
		else:
			compiledParts.extend(self.__compilePart(parts[0]))
			compiledParts.append(".*")
			compiledParts.extend(self.__compilePart(parts[1]))

		compiledParts.append("$")

		sREPattern = "".join(compiledParts)
		#print(sREPattern)
		self.__p = re.compile(sREPattern)

		self.__orgPattern = pattern
	#

	################################################################################################################################
	## Public Property
	################################################################################################################################

	@property
	def pattern(self) -> str:
		return self.__orgPattern
	#

	################################################################################################################################
	## Helper Method
	################################################################################################################################

	def __compilePart(self, part:str):
		for c in part:
			if c == "?":
				yield "."
				continue
			if c in "\\.[](){}-+":
				yield "\\" + c
				continue
			yield c
	#

	################################################################################################################################
	## Public Method
	################################################################################################################################

	def match(self, text) -> bool:
		if not isinstance(text, str):
			text = text.__str__()
		return self.__p.match(text) is not None
	#

	def __str__(self):
		return self.__orgPattern
	#

	def __repr__(self):
		return "FileNamePattern<({})>".format(repr(self.__orgPattern))
	#

#





