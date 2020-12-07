



import os
import random
import typing

import jk_typing





class SecureRandomIDGenerator(object):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self):
		self.__reservoir = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		assert len(self.__reservoir) == 26 + 26 + 10
		self.__rng = random.Random(os.urandom(32))
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def generateID(self, countChars:int) -> str:
		assert countChars > 0
		
		return "".join([ self.__rng.choice(self.__reservoir) for i in range(0, countChars) ])
	#

#















