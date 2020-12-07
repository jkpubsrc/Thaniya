

import re
import time
import os
import typing

import jk_typing
import jk_logging
import jk_prettyprintobj

from thaniya_common.utils import IOContext

from .JobFile import JobFile







#
# Represents a job loaded at runtime
#
class JobQueueInlet(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, ioContext:IOContext, dirPath:str, log:jk_logging.AbstractLogger = None):
		self.__ioContext = ioContext

		if log:
			log.notice("Job queue inlet using directory: " + dirPath)
		self.__jobDirPath = dirPath
		assert os.path.isdir(dirPath)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __createJobIDAndFilePath(self) -> str:
		tLast = -1
		while True:
			while True:
				tNow = int(time.time() * 1000000)
				if tNow != tLast:
					break
			tLast = tNow
			jobID = "{:0>16x}".format(tNow)
			jobFilePath = os.path.join(self.__jobDirPath, jobID + "-job.json")
			if not os.path.exists(jobFilePath):
				return jobID, jobFilePath
	#

	def _dumpVarNames(self) -> list:
		return [
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Create a new job
	#
	@jk_typing.checkFunctionSignature()
	def scheduleJob(self, jobType:str, jobPriority:int, jobData:dict):
		jobFile = JobFile.create(jobType, jobPriority, jobData)
		jobID, jobFilePath = self.__createJobIDAndFilePath()
		jobFile.writeToFile(jobFilePath)
	#

#









