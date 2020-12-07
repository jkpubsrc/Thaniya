


import time
import typing
import hashlib
import collections
import threading

import jk_typing

from ..utils.APIError import APIError
from ._auth_common import _Resp, _checkBytesEqual
from ..usermgr.BackupUser import BackupUser






_AuthAttempt = collections.namedtuple("_AuthAttempt", [
	"asid",								# authentification session ID;
	"t",								# time stamp;
	"auth",								# the authentification method object;
	"userName",							# the name of the user that tries to authenticate;
	"peerFingerprint",					# some kind of fingerprint that represents the connecting peer;
	"serverData",						# server data that is required by the authentification method; this data is NOT sent to the client;
])





class APIAuthentificator(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, appRuntime, timeOutSeconds:int):
		assert appRuntime is not None
		assert appRuntime.__class__.__name__ == "AppRuntimeUploadHttpd"
		assert isinstance(timeOutSeconds, int)
		assert timeOutSeconds > 0
		self.__timeOutSeconds = timeOutSeconds

		# ----

		self.__appRuntime = appRuntime

		self.__authMethods = {}

		from .Auth_Basic_SHA2_256 import Auth_Basic_SHA2_256
		self.__registerAuthMethod(Auth_Basic_SHA2_256())

		self.__lock = threading.Lock()

		self.__authAttempts = {}				# stores runtime data
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __registerAuthMethod(self, auth):
		self.__authMethods[auth.identifier] = auth
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def cleanup(self):
		with self.__lock:
			keysToRemove = []

			tNow = time.time()
			for a in self.__authAttempts.values():
				if tNow - a.t > self.__timeOutSeconds:
					keysToRemove.append(a.identifier)

			for identifier in keysToRemove:
				del self.__data[identifier]
	#

	#
	# The method is called if the client wants to initiate a test that it has the correct password.
	# This caller expects to receive data that is to return to the remote peer.
	#
	# @param		backupUser BackupUser			(required) The user that tries to authenticate
	# @param		str peerFingerprint				(required) Some kind of fingerprint that represents the connecting peer. This string could be generated from
	#												the peer's IP address or other connection data. It must be identical for every connection exected by this
	#												peer during this session.
	# @param		str authMethod					(required) An ID that represents the authentification method the client wishes to use.
	# @return		dict							This method returns JSON data that can be sent to the client.
	#												An exception might occur but is not typical.
	#
	@jk_typing.checkFunctionSignature()
	def onClientConnect(self, peerFingerprint:str, userName:str, authMethod:str) -> dict:
		backupUser = self.__appRuntime.userMgr.getUserE(userName)

		if not backupUser.enabled:
			raise APIError("errAccountDisabled")

		if not backupUser.canUpload:
			raise APIError("errAccountUnprepared")

		with self.__lock:
			auth = self.__authMethods.get(authMethod)
			if auth is None:
				raise APIError("errAuthMethod")

		resp = auth.onClientConnect(self.__appRuntime, backupUser)

		a = _AuthAttempt(
			self.__appRuntime.secureIDGen.generateID(32),
			time.time(),
			auth,
			backupUser.userName,
			peerFingerprint,
			resp.serverData,
		)

		with self.__lock:
			self.__authAttempts[a.asid] = a

		clientData = resp.clientData
		clientData["asid"] = a.asid
		return clientData
	#

	#
	# This method is called if the client wants to testify that it has the correct password.
	# This caller expects either to have an exception raised or a <c>True</c> to indicate success.
	#
	# @param		str peerFingerprint				(required) Some kind of fingerprint that represents the connecting peer. This string could be generated from
	#												the peer's IP address or other connection data. It must be identical for every connection exected by this
	#												peer during this session.
	# @param		dict clientResponseData			(required) The data that the client sent to confirm knowledge of the password.
	# @return		str								Raises an exception on error, returns the user name on success.
	#
	@jk_typing.checkFunctionSignature()
	def onClientResponse(self, peerFingerprint:str, clientResponseData:dict) -> str:
		asid = clientResponseData["asid"]

		try:
			with self.__lock:
				if asid not in self.__authAttempts:
					raise APIError("errInvalidASID")

				a = self.__authAttempts[asid]

				tSpan = time.time() - a.t
				if tSpan > self.__timeOutSeconds:
					raise APIError("errTimeout")

				backupUser = self.__appRuntime.userMgr.getUser(a.userName)
				if backupUser is None:
					raise APIError("errNoSuchUser")

				if a.peerFingerprint != peerFingerprint:
					print("Fingerprints differ!")
					raise APIError("errAuthInvalid")

				if a.auth.onClientResponse(self.__appRuntime, backupUser, a.serverData, clientResponseData) is not True:
					print("onClientResponse failed!")
					raise APIError("errAuthInvalid")

				# success
				return a.userName

		finally:
			del self.__authAttempts[asid]
	#

#













