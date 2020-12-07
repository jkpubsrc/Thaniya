


import json

import jk_json
import jk_typing
from jk_utils import AmountOfBytes

from thaniya_common.cfg import CfgKeyValueDefinition
from thaniya_common.cfg import AbstractCfgComponent
from thaniya_common.cfg import AbstractAppCfg
from thaniya_common.cfg import CfgComponent_Magic








class _Magic(CfgComponent_Magic):

	MAGIC = "thaniya-job"
	VERSION = 1
	VALID_VERSIONS = [ 1 ]

#





class _DataV1(AbstractCfgComponent):

	__VALID_KEYS = [
		# NOTE: Convetion: all data provided by clients that might be untrue are marked with "Client"

		CfgKeyValueDefinition("jobType",			str,	False			),	# This defines the type of the job (and at the same time the interpreter that will process this job)
		CfgKeyValueDefinition("jobPriority",		int,	False			),
		CfgKeyValueDefinition("jobData",			dict,	False			),	# The job data that will be interpreted later
	]

	def __init__(self):
		super().__init__(_DataV1.__VALID_KEYS)

		self._jobType = None				# str
		self._jobPriority = None			# int
		self._jobData = None				# str
	#

#





#
# Represents the contents of a job file.
#
class JobFile(AbstractAppCfg):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self):
		super().__init__(
			_Magic,
			False,
			{
				"data": _DataV1(),
			}
		)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def jobType(self) -> str:
		return self._groups["data"]._jobType
	#

	@property
	def jobPriority(self) -> int:
		return self._groups["data"]._jobPriority
	#

	@property
	def jobData(self) -> dict:
		return self._groups["data"]._jobData
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Public Static Methods
	################################################################################################################################

	@staticmethod
	@jk_typing.checkFunctionSignature()
	def loadFromFile(filePath:str):
		assert isinstance(filePath, str)

		jData = jk_json.loadFromFile(filePath)

		ret = JobFile()
		ret._loadFromJSON(jData)

		return ret
	#

	@staticmethod
	@jk_typing.checkFunctionSignature()
	def create(jobType:str, jobPriority:int, jobData:dict):
		ret = JobFile()
		ret.setValue("data", "jobType", jobType)
		ret.setValue("data", "jobPriority", jobPriority)
		ret.setValue("data", "jobData", jobData)
		return ret
	#

#









