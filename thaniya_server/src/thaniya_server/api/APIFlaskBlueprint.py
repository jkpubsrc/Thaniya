

import typing
import functools

import jk_exceptionhelper
import jk_typing

import flask
import flask_login

from ..utils.APIError import APIError
from .APIMethodContext import APIMethodContext
from ..session.MemorySessionManager import MemorySessionManager
from ..usermgr.BackupUser import BackupUser
from ..usermgr.BackupUserManager import BackupUserManager










class APIFlaskBlueprint(flask.Blueprint):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, app:flask.Flask, import_name:str, appRuntime, sessionMgr:MemorySessionManager, userMgr:BackupUserManager, url_prefix:str):
		super().__init__("api", import_name, url_prefix=url_prefix)

		self.app = app
		self.appRuntime = appRuntime
		self.apiSessionMgr = sessionMgr
		self.userMgr = userMgr
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __getPeerFingerprint(self, request:flask.Request, remoteAddr:str) -> str:
		userAgent = request.environ.get("HTTP_USER_AGENT", "")

		accept = request.environ.get("HTTP_ACCEPT", "")

		acceptLanguage = request.environ.get("HTTP_ACCEPT_LANGUAGE", "")

		return "|".join([remoteAddr, userAgent, accept, acceptLanguage])
	#

	def __getRemoteAddr(self, request:flask.Request) -> str:
		s = request.environ.get("HTTP_X_FORWARDED_FOR")
		if s:
			return s
		s = request.environ.get("REMOTE_ADDR")
		if s:
			return s
		s = request.remote_addr
		if s:
			return s
		raise Exception()
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def apiCall(self, bAuthRequired:bool = False):
	
		def my_decorator(f):

			@functools.wraps(f)
			def decorated_function(*args, **kwargs):
				jResponse = None
				try:
					request = flask.request
					remoteAddr = self.__getRemoteAddr(request)
					peerFingerprint = self.__getPeerFingerprint(request, remoteAddr)

					# print some debugging output

					print("=" * 160)
					print("==== base_url:", request.base_url)
					print("==== peerFingerprint:", peerFingerprint)

					for k, v in request.headers:
						print("==", k, ":", v)

					# retrieve the data sent by the client

					if request.method == "GET":
						jData = request.args.to_dict()
					elif request.method == "POST":
						jData = request.get_json()
						if (jData is None) or not isinstance(jData, dict):
							raise APIError("errRequest")
					else:
						raise APIError("errRequest")

					# print incoming data sent by the client

					print("¦>> {")
					for key, value in jData.items():
						print("¦>>\t", key, "=", repr(value))
					print("¦>> }")

					# let's isolate the session ID and get user name and session data

					sessionData = None
					userName = None
					if "sid" in jData:
						sid = jData["sid"]
						if not isinstance(sid, str):
							raise APIError("errRequest")
						del jData["sid"]

						userName, sessionData = self.apiSessionMgr.get(sid, peerFingerprint, True)
						if userName is None:		# None indicates that the session does not exist or has timed out
							# let's assume the client did not send a session ID;
							# this way *if* we have to deal with a session ID we always will have a valid one from now on;
							sid = None
					else:
						sid = None

					# if we have a valid session ID, get the user object

					user = None
					if sid is None:
						if bAuthRequired:
							raise APIError("errNotAuth")
					else:
						user = self.userMgr.getUserE(userName)

					# call the API method

					ctx = APIMethodContext(self.appRuntime, request, remoteAddr, peerFingerprint, jData, user, sid, sessionData)
					newArgs = ( ctx, ) + args
					ret = f(*newArgs, **kwargs)

					# create the success response data

					jResponse = {
						"success": True,
						"data": ret
					}

				except APIError as ee:
					# something failed; create the error response data
					jResponse = {
						"errID": ee.errID
					}

				except Exception as ee:
					# something failed seriously and unexpectedly; create the error response data
					eobj = jk_exceptionhelper.analyseException(ee)
					eobj.dump()

					jResponse = {
						"errID": "errUnexpected"
					}

				# print the data we are going to return

				print("<<¦ {")
				for key, value in jResponse.items():
					print("<<¦ \t", key, "=", repr(value))
				print("<<¦ }")

				# return the data

				return flask.jsonify(jResponse)
			#

			return decorated_function
		#

		return my_decorator
	#

#












