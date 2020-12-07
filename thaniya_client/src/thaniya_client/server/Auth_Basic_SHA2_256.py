


import time
import typing
import hashlib
import collections

import jk_typing
import jk_utils









class Auth_Basic_SHA2_256(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, userName:str, password:str):
		self.__userName = userName
		self.__bytesPwd = jk_utils.Bytes(password)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def identifier(self) -> str:
		return "basic-sha2-256"
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def onServerResponse(self, jData:dict) -> dict:
		asid = jData["asid"]
		serverRandDataBytes = jk_utils.Bytes(jData["rand"])

		h = hashlib.sha256()
		h.update(bytes(serverRandDataBytes))
		h.update(bytes(self.__bytesPwd))
		pwdHashedBytes = jk_utils.Bytes(h.digest())

		return {
			"asid": asid,
			"hashed": str(pwdHashedBytes),
		}
	#

#













