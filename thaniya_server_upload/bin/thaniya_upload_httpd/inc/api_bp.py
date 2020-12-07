

from typing import Union
from functools import wraps

import jk_exceptionhelper
import jk_logging
import jk_utils
import jk_typing

import flask
import flask_login

from thaniya_server.usermgr import BackupUser
from thaniya_server.usermgr import BackupUserManager
from thaniya_server.api import APIMethodContext
from thaniya_server.api import APIFlaskBlueprint
from thaniya_server.utils import APIError

from thaniya_server_upload.slots import UploadSlot
from thaniya_server_upload import AppRuntimeUploadHttpd















@jk_typing.checkFunctionSignature()
def init_blueprint(app:flask.Flask, appRuntime:AppRuntimeUploadHttpd, log:jk_logging.AbstractLogger):

	api_bp = APIFlaskBlueprint(app, __name__, appRuntime, appRuntime.apiSessionMgr, appRuntime.userMgr, url_prefix="/api/v1")

	# --------------------------------------------------------------------------------------------------------------------------------

	@api_bp.route("/noop", methods=[ "GET", "POST" ])
	@api_bp.apiCall()
	def api_noop(ctx:APIMethodContext):
		if ctx.sid:
			s = "noop (" + ctx.sid + ")"
		else:
			s = "noop ()"

		print(s)
		return True
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@api_bp.route("/noopAuth", methods=[ "GET", "POST" ])
	@api_bp.apiCall(bAuthRequired=True)
	def api_noopAuth(ctx:APIMethodContext):
		if ctx.sid:
			s = "noopAuth (" + ctx.sid + ")"
		else:
			s = "noopAuth ()"

		print(s)
		return True
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@api_bp.route("/auth1", methods=[ "GET", "POST" ])
	@api_bp.apiCall()
	def api_auth1(ctx:APIMethodContext):
		userName = ctx.jData.get("userName")
		authMethod = ctx.jData.get("authMethod")
		if (not userName) or (not authMethod):
			raise APIError("errArgs")

		return appRuntime.apiAuth.onClientConnect(ctx.peerFingerprint, userName, authMethod)
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@api_bp.route("/auth2", methods=[ "GET", "POST" ])
	@api_bp.apiCall()
	def api_auth2(ctx:APIMethodContext):
		userName = appRuntime.apiAuth.onClientResponse(ctx.peerFingerprint, ctx.jData)
		assert isinstance(userName, str)

		# create API session

		apiSessionID = appRuntime.apiSessionIDGen.generateSessionID()
		appRuntime.apiSessionMgr.put(apiSessionID, ctx.peerFingerprint, userName, {})

		return {
			"sid": apiSessionID
		}
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@api_bp.route("/uploadStats", methods=[ "GET", "POST" ])
	@api_bp.apiCall(bAuthRequired=True)
	def uploadStats(ctx:APIMethodContext):
		nSlotsAllocated = 0
		nSlotsInUse = 0
		nSlotsFree = 0
		nSlotsTotal = 0
		for slot in appRuntime.uploadSlotMgr.slots:
			assert isinstance(slot, UploadSlot)
			nSlotsTotal += 1
			if slot.isReady:
				nSlotsFree += 1
			if slot.isAllocated:
				nSlotsAllocated += 1
			if slot.isInUseByClient:
				nSlotsInUse += 1

		fsStats = appRuntime.uploadSlotMgr.getFileSystemStats()			# jk_utils.fsutils.FileSystemStats

		spaceMargin = appRuntime.uploadSlotMgr.fsSecuritySpaceMarginBytes
		bytesFree = max(0, fsStats.bytesFreeUser - spaceMargin)

		return {
			"slots": {
				"nAllocated": nSlotsAllocated,
				"nInUse": nSlotsInUse,
				"nFree": nSlotsFree,
				"nTotal": nSlotsTotal,
			},
			"uploadDiskspace": {
				"totalBytes": fsStats.bytesTotal,
				"usedBytes": fsStats.bytesTotal - bytesFree,
				"freeBytes": bytesFree,
				"filledRatio": fsStats.rateBytesUsed,
			},
		}
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@api_bp.route("/allocateSlot", methods=[ "GET", "POST" ])
	@api_bp.apiCall(bAuthRequired=True)
	def allocateSlot(ctx:APIMethodContext):
		nEstimatedTotalBytesToUpload = ctx.jData["estimatedTotalBytesToUpload"]
		assert isinstance(nEstimatedTotalBytesToUpload, int)

		jClientData = appRuntime.uploadSlotMgr.allocateSlot(ctx.user, ctx.remoteAddr, nEstimatedTotalBytesToUpload, log)
		return jClientData
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	@api_bp.route("/uploadCompleted", methods=[ "GET", "POST" ])
	@api_bp.apiCall(bAuthRequired=True)
	def uploadCompleted(ctx:APIMethodContext):
		bSuccess = ctx.jData["success"]
		assert isinstance(bSuccess, bool)

		uploadSlotID = ctx.jData["slotID"]

		if bSuccess:
			appRuntime.uploadSlotMgr.finalizingUpload(ctx.user, uploadSlotID, log)
		else:
			appRuntime.uploadSlotMgr.resetSlot(ctx.user, uploadSlotID, log)

		return None
	#

	# --------------------------------------------------------------------------------------------------------------------------------

	app.register_blueprint(api_bp)

#















