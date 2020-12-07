

import os
import typing
import copy

import jk_typing
import jk_json
import jk_prettyprintobj

from .JobFile import JobFile
from .EnumJobState import EnumJobState






#
# This class is a generic job used at runtime. It is managed by the job queue.
#
class Job(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, jobQueue, jobFile:JobFile, jobID:str, filePath:str):
		self.__jobQueue = jobQueue
		self.__jobFile = jobFile
		self.__jobFilePath = filePath
		self.__jobID = jobID

		self.__processingStateFilePath = os.path.join(os.path.dirname(self.__jobFilePath), jobID + "-state.json")
		if os.path.isfile(self.__processingStateFilePath):
			self.__processingState = jk_json.loadFromFile(self.__processingStateFilePath)
		else:
			self.__processingState = {
				"state": EnumJobState.READY.value,
				"data": {},
			}
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def jobID(self) -> str:
		return self.__jobID
	#

	@property
	def jobType(self) -> str:
		return self.__jobFile.jobType
	#

	@property
	def jobPriority(self) -> int:
		return self.__jobFile.jobPriority
	#

	@property
	def jobData(self) -> dict:
		return copy.deepcopy(self.__jobFile.jobData)
	#

	@property
	def state(self) -> EnumJobState:
		return EnumJobState(self.__processingState["state"])
	#

	@state.setter
	def state(self, value:EnumJobState):
		assert isinstance(value, EnumJobState)
		self.__processingState["state"] = value.value
	#

	@property
	def processingStateData(self) -> dict:
		return self.__processingState["data"]
	#

	#@property
	#def filePath(self) -> str:
	#	return self.__jobFilePath
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"jobID",
			#"filePath",
			"jobType",
			"jobPriority",
			"jobData",
			"state",
			"processingStateData",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def tryReload(self) -> bool:
		if os.path.isfile(self.__jobFilePath):
			try:
				self.__jobFile._loadFromJSON(jk_json.loadFromFile(self.__jobFilePath))

				if os.path.isfile(self.__processingStateFilePath):
					self.__processingState = jk_json.loadFromFile(self.__processingStateFilePath)
				else:
					pass
					# in this case we keep the existing data.

				return True
			except:
				return False
		else:
			return False
	#

	def storeProcessingState(self):
		jk_json.saveToFilePretty(self.__processingState, self.__processingStateFilePath + ".tmp")
		if os.path.isfile(self.__processingStateFilePath):
			os.unlink(self.__processingStateFilePath)
		os.rename(self.__processingStateFilePath + ".tmp", self.__processingStateFilePath)
	#

	def destroy(self):
		if os.path.isfile(self.__processingStateFilePath):
			os.unlink(self.__processingStateFilePath)
		if os.path.isfile(self.__jobFilePath):
			os.unlink(self.__jobFilePath)
		if self.__jobQueue:
			self.__jobQueue._removeJobFromQueue(self)
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#


















