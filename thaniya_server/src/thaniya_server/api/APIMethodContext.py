

import typing

import jk_typing

import flask
import flask_login

from ..utils import APIError
from ..usermgr import BackupUser










class APIMethodContext(object):

	__slots__ = (
		"_appRuntime",
		"_request",
		"_remoteAddr",
		"_peerFingerprint",
		"_jData",
		"_user",
		"_sid",
		"_sessionData",
	)

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self,
			appRuntime,				# AppRuntimeUploadHttpd
			request,				# flask.Request
			remoteAddr:str,
			peerFingerprint:str,
			jData:dict,
			user:typing.Union[BackupUser,None],
			sid:typing.Union[str,None],
			sessionData:typing.Union[dict,None],
		):

		self._appRuntime = appRuntime
		self._request = request
		self._remoteAddr = remoteAddr
		self._peerFingerprint = peerFingerprint
		self._jData = jData
		self._user = user
		self._sid = sid
		self._sessionData = sessionData
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def remoteAddr(self):
		return self._remoteAddr
	#

	#
	# The central application runtime object
	#
	@property
	def appRuntime(self):
		return self._appRuntime
	#

	#
	# The flask request object
	#
	@property
	def request(self) -> flask.Request:
		return self._request
	#

	#
	# A fingerprint generated from the peer that sent this API request
	#
	@property
	def peerFingerprint(self) -> str:
		return self._peerFingerprint
	#

	#
	# This is the data that is sent with the API request
	#
	@property
	def jData(self) -> dict:
		return self._jData
	#

	#
	# If we have a session this property returns the user object
	#
	@property
	def user(self) -> typing.Union[BackupUser,None]:
		return self._user
	#

	#
	# If we have a session this property returns the session ID
	#
	@property
	def sid(self) -> typing.Union[str,None]:
		return self._sid
	#

	#
	# If we have a session this property gives access to the session data
	#
	@property
	def sessionData(self) -> typing.Union[dict,None]:
		return self._sessionData
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#










