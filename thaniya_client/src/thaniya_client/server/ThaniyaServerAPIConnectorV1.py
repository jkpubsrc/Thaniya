

import requests
import json
import typing

import jk_typing
import jk_json



from .Auth_Basic_SHA2_256 import Auth_Basic_SHA2_256







class ThaniyaServerAPIConnectorV1(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, hostName:str, port:int):
		self.__hostName = hostName
		self.__port = port
		self.__sid = None

		self.__basUrl = "http://" + hostName + ":" + str(port) + "/api/v1/"
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __performPOSTRequest(self, apiCmd:str, jData:dict):
		assert isinstance(apiCmd, str)
		assert isinstance(jData, dict)

		targetURL = self.__basUrl + apiCmd

		print("=" * 160)
		print("==== " + targetURL)

		if self.__sid:
			jData["sid"] = self.__sid

		for line in json.dumps(jData, indent="\t", sort_keys=True).split("\n"):
			print("¦>> " + line)

		r = requests.post(targetURL, json=jData)
		if r.status_code != 200:
			raise Exception("errResponse")

		jData = r.json()

		for line in jk_json.dumps(jData, indent="\t", sort_keys=True).split("\n"):
			print("<<¦ " + line)

		if not isinstance(jData, dict):
			raise Exception("errResponse")

		if "success" not in jData:
			jk_json.prettyPrint(jData)
			raise Exception("errResponse")

		return jData["data"]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def noop(self):
		self.__performPOSTRequest("noop", {})
	#

	def noopAuth(self):
		self.__performPOSTRequest("noopAuth", {})
	#

	def authenticate(self, userName:str, password:str):
		a = Auth_Basic_SHA2_256(userName, password)

		r = self.__performPOSTRequest("auth1", {
			"userName": userName,
			"authMethod": a.identifier,
		})

		r = a.onServerResponse(r)

		r = self.__performPOSTRequest("auth2", r)

		self.__sid = r["sid"]
	#

	def uploadStats(self) -> dict:
		return self.__performPOSTRequest("uploadStats", {})
	#

	@jk_typing.checkFunctionSignature()
	def allocateSlot(self, estimatedTotalBytesToUpload:int) -> dict:
		return self.__performPOSTRequest("allocateSlot", {
			"estimatedTotalBytesToUpload": estimatedTotalBytesToUpload
		})
	#

	@jk_typing.checkFunctionSignature()
	def uploadCompleted(self, uploadSlotID:str, bSuccess:bool):
		return self.__performPOSTRequest("uploadCompleted", {
			"slotID": uploadSlotID,
			"success": bSuccess,
		})
	#

#















