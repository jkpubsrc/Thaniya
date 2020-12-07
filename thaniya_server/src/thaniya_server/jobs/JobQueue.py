

import re
import time
import os
import typing

import jk_typing
import jk_logging
import jk_prettyprintobj

from thaniya_common.utils import IOContext

from .EnumJobState import EnumJobState
from .JobFile import JobFile
from .Job import Job







#
# Represents a job loaded at runtime
#
class JobQueue(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, ioContext:IOContext, dirPath:str, bResetJobStateOnLoad:bool, log:jk_logging.AbstractLogger):
		self.__ioContext = ioContext

		log.notice("Job queue directory: " + dirPath)
		self.__jobDirPath = dirPath
		assert os.path.isdir(dirPath)

		ioContext.setDirMode(dirPath)

		self.__bResetJobStateOnLoad = bResetJobStateOnLoad

		self.__jobsByPriority = {}
		self.__jobsByID = {}

		# ----

		self.update(log)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# Returns a list of all jobs.
	#
	@property
	def jobs(self) -> typing.List[Job]:
		return list(self.__jobsByID.values())
	#

	@property
	def jobPriorities(self) -> typing.List[int]:
		return sorted(self.__jobsByPriority.keys())
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def ____addJob(self, job:Job):
		if job.jobID in self.__jobsByID:
			return

		jobList = self.__jobsByPriority.get(job.jobPriority)
		if jobList is None:
			jobList = []
			self.__jobsByPriority[job.jobPriority] = jobList
		jobList.append(job)

		self.__jobsByID[job.jobID] = job
	#

	def ____removeJob(self, job:Job):
		if job.jobID not in self.__jobsByID:
			return

		jobList = self.__jobsByPriority.get(job.jobPriority)
		if jobList is None:
			# that's strange!
			pass
		else:
			jobList.remove(job)

		del self.__jobsByID[job.jobID]
	#

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

	def _removeJobFromQueue(self, job:Job):
		self.____removeJob(job)
	#

	def _dumpVarNames(self) -> list:
		return [
			"jobs",
			"jobPriorities",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def getNextWaitingJob(self) -> typing.Union[Job,None]:
		for jobPriority in sorted(self.__jobsByPriority.keys(), reverse=True):		# highest to lowest priority
			jobList = self.__jobsByPriority[jobPriority]
			for job in jobList:
				if job.state == EnumJobState.READY:
					return job
		return None
	#

	#
	# Create a new job
	#
	@jk_typing.checkFunctionSignature()
	def scheduleJob(self, jobType:str, jobPriority:int, jobData:dict) -> Job:
		jobFile = JobFile.create(jobType, jobPriority, jobData)
		jobID, jobFilePath = self.__createJobIDAndFilePath()
		jobFile.writeToFile(jobFilePath)

		job = Job(self, jobFile, jobID, jobFilePath)

		self.____addJob(job)

		return job
	#

	"""
	#
	# Reload everything that exists, discard jobs that are gone, and load all missing job files from disk.
	#
	def refresh(self, log:jk_logging.AbstractLogger):
		jobsToDelete = []

		for job in self.__jobsByID.values():
			if not job.tryReload():
				jobsToDelete.append(job)

		for job in jobsToDelete:
			del self.__jobsByID[job.jobID]
			self.__jobsByPriority[job.jobPriority].remove(job)

		self.update(log)
	#
	"""

	#
	# Load all job files from disk that we do not yet know about
	#
	def update(self, log:jk_logging.AbstractLogger):
		log.notice("Scanning for jobs to load ...")

		# select all job files we do not yet know about
		jobIDPathTuples = []
		for fe in os.scandir(self.__jobDirPath):
			if fe.is_file():
				m = re.match("^(.+)-job.json$", fe.name)
				if m:
					jobID = m.group(1)
					if jobID not in self.__jobsByID:
						jobIDPathTuples.append((jobID, fe.path))

		# order them in ascending order
		jobIDPathTuples = sorted(jobIDPathTuples, key=lambda x: x[0])

		# load all jobs
		for jobID, jobFilePath in jobIDPathTuples:
			log.notice("Loading job from file: " + jobFilePath)
			jobFile = JobFile.loadFromFile(jobFilePath)
			job = Job(self, jobFile, jobID, jobFilePath)
			if self.__bResetJobStateOnLoad:
				if job.state != EnumJobState.READY:
					log.notice("Resetting job: " + job.jobID)
					job.state = EnumJobState.READY
					job.storeProcessingState()
					# NOTE: We do NOT reset the processing state data. The processing state data might contain useful information.
			self.____addJob(job)
	#

#


















