

import os
import typing

import jk_typing

from .FileNamePattern import FileNamePattern
from .ProcessingRule import ProcessingRule












class ProcessingRuleSet(object):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, processingRules:list):
		self.__processingRules = processingRules
	#

	################################################################################################################################
	## Public Property
	################################################################################################################################

	@property
	def processingRules(self) -> list:
		return self.__processingRules
	#

	################################################################################################################################
	## Helper Method
	################################################################################################################################

	################################################################################################################################
	## Public Method
	################################################################################################################################

	#
	# Tries to find a suitable processing rule.
	#
	def tryMatch(self, filePathOrName:str) -> typing.Union[ProcessingRule,None]:
		assert isinstance(filePathOrName, str)

		fileName = os.path.basename(filePathOrName)
		for rule in self.__processingRules:
			assert isinstance(rule, ProcessingRule)
			if rule.fileNamePattern.match(fileName):
				return rule

		return None
	#

#










