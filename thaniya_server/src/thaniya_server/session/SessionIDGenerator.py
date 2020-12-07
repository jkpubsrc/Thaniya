



import os
import random
import typing

import jk_typing







class SessionIDGenerator(object):

	__CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

	################################################################################################################################
	## Constructors
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, sessionIDLength:int = None):
		if sessionIDLength is None:
			sessionIDLength = 16
		else:
			assert sessionIDLength >= 12

		# ----

		self.__rng = random.Random(os.urandom(32))

		self.__sessionIDLength = sessionIDLength
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Generate a new session ID of good random quality.
	#
	def generateSessionID(self) -> str:
		return "".join([ self.__rng.choice(SessionIDGenerator.__CHARACTERS) for i in range(0, self.__sessionIDLength) ])
	#

#















