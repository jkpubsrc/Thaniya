


import sys
import binascii
import os
import random
import typing
import base64

import jk_typing
import jk_utils




class _APIPasswordGenerator():

	def __init__(self):
		self.__reservoir = None
		self.__rng = None
	#

	def createHexData(self, countBytes:int) -> str:
		assert isinstance(countBytes, int)
		assert countBytes >= 2

		if not self.__reservoir:
			self.__reservoir = "abcdef0123456789"
			assert len(self.__reservoir) == 16
			self.__rng = random.Random(os.urandom(32))

		return "".join([ self.__rng.choice(self.__reservoir) for i in range(0, countBytes*2) ])
	#

#

_GEN = _APIPasswordGenerator()








#
# This is a convenience wrapper around an array of bytes.
#
class APIPassword(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, data):
		if isinstance(data, (bytes,bytearray)):
			self.__rawByteData = bytes(data)
		elif isinstance(data, str):
			if data.startswith("x:"):
				self.__rawByteData = binascii.unhexlify(data[2:].encode("ascii"))
			elif data.startswith("64:"):
				self.__rawByteData = base64.b64decode(data[3:])
			else:
				raise Exception("This is not a valid string representation of a password.")
		else:
			raise Exception()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def hexStr(self):
		return "x:" + binascii.hexlify(self.__rawByteData).decode("ascii")
	#

	def toHexStr(self):
		return "x:" + binascii.hexlify(self.__rawByteData).decode("ascii")
	#

	def base64Str(self):
		return "64:" + base64.b64encode(self.__rawByteData).decode("ascii")
	#

	def toBase64Str(self):
		return "64:" + base64.b64encode(self.__rawByteData).decode("ascii")
	#

	def __repr__(self):
		return "APIPassword<(" + self.__str__() + ")>"
	#

	def __bytes__(self):
		return self.__rawByteData
	#

	def __str__(self):
		return self.base64Str()
	#

	def __add__(self, other):
		assert isinstance(other, APIPassword)
		return APIPassword(self.__rawByteData + other.__rawByteData)
	#

	def __len__(self):
		return len(self.__rawByteData)
	#

	def __eq__(self, other):
		if isinstance(other, APIPassword):
			return self.__rawByteData == other.__rawByteData
		elif isinstance(other, (bytes, bytearray)):
			return self.__rawByteData == other
		else:
			return False
	#

	def __ne__(self, other):
		if isinstance(other, APIPassword):
			return self.__rawByteData != other.__rawByteData
		elif isinstance(other, (bytes, bytearray)):
			return self.__rawByteData != other
		else:
			return False
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	@staticmethod
	def generate(countBytes:int = 64):
		assert isinstance(countBytes, int)
		assert countBytes >= 2

		return APIPassword("x:" + _GEN.createHexData(countBytes))
	#

#
















