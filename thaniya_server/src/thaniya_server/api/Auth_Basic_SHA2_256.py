


import time
import typing
import hashlib
import collections

import jk_typing
import jk_utils

from ..usermgr.BackupUser import BackupUser
from ._auth_common import _Resp, _checkBytesEqual








class Auth_Basic_SHA2_256(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		pass
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

	# TODO: implement an interface to specify a type appRuntime must match against
	@jk_typing.checkFunctionSignature()
	def onClientConnect(self, appRuntime, backupUser:BackupUser) -> _Resp:
		randDataBytes = appRuntime.secureRNG.generateBytes(64)

		return _Resp({
			"randBytes": randDataBytes,
		}, {
			"rand": str(randDataBytes)
		})
	#

	@jk_typing.checkFunctionSignature()
	def onClientResponse(self, appRuntime, backupUser:BackupUser, serverData:dict, clientResponseData:dict) -> bool:
		serverRandDataBytes = serverData["randBytes"]			# Bytes
		assert isinstance(serverRandDataBytes, jk_utils.Bytes)

		bytesPwd = jk_utils.Bytes(backupUser.uploadPwd)

		clientBytesHashed = jk_utils.Bytes(clientResponseData["hashed"])
		#print("clientBytesHashed =", clientBytesHashed)

		h = hashlib.sha256()
		h.update(bytes(serverRandDataBytes))
		h.update(bytes(bytesPwd))
		serverBytesHashed = jk_utils.Bytes(h.digest())
		#print("serverBytesHashed =", serverBytesHashed)
		#print("length =", len(bytes(serverBytesHashed)))
		#print("length =", len(serverBytesHashed))

		ret = _checkBytesEqual(bytes(clientBytesHashed), bytes(serverBytesHashed), 32)
		#print("ret =", ret)
		return ret
	#

#













