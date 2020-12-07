


import os
import typing
import time
import threading

import jk_typing
import jk_utils
import jk_logging
import jk_prettyprintobj

from .EnumJobState import EnumJobState
from .Job import Job
from .JobProcessingCtx import JobProcessingCtx
from .AbstractJobProcessor import AbstractJobProcessor
from .JobQueue import JobQueue








class JobProcessingEngine(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, log:jk_logging.AbstractLogger, **kwargs):
		self.__jobProcessors = {}
		self.__ctxData = kwargs
		self.__jobQueue = None
		self.__t = None
		self.__bTerminate = False
		self.__terminationFlag = jk_utils.TerminationFlag()
		self.__log = log

		self.__currentJob = None
		self.__currentJobCtx = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def jobContextData(self) -> dict:
		return self.__ctxData
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
		]
	#

	def __runJob(self, job:Job, jobProcessor:AbstractJobProcessor, log:jk_logging.AbstractLogger):
		try:
			# create job processing context

			self.__currentJobCtx = JobProcessingCtx(
				terminationFlag = self.__terminationFlag,
				log = log,
				**self.__ctxData)
			self.__currentJob = job

			# update job state

			job.state = EnumJobState.PROCESSING
			job.errInfo = None
			job.storeProcessingState()

			# now process the job

			resultState = None				# EnumJobState
			try:
				jobProcessor.processJob(self.__currentJobCtx, self.__currentJob)
				resultState = EnumJobState.SUCCESS
			except jk_utils.InterruptedException as ee:
				log.exception(ee)
				resultState = EnumJobState.INTERRUPTED
			except jk_logging.ExceptionInChildContextException as ee:
				# NOTE: don't log this exception as it has already been logged
				if isinstance(ee.originalExeption, jk_utils.InterruptedException):
					resultState = EnumJobState.INTERRUPTED
				else:
					log.exception(ee.originalException)
			except Exception as ee:
				log.exception(ee)
				resultState = EnumJobState.ERROR

			# update job state

			job.state = resultState
			job.storeProcessingState()

			# result actions

			if resultState is EnumJobState.SUCCESS:
				log.success("Job succeeded: " + job.jobID)
			elif resultState is EnumJobState.INTERRUPTED:
				log.error("Job interrupted: " + job.jobID)
			elif resultState is EnumJobState.ERROR:
				log.error("Job failed: " + job.jobID)
			else:
				# we should never arrive at other states than those listed above!
				raise jk_utils.ImplementationError()

		finally:
			self.__currentJob = None
			self.__currentJobCtx = None
	#

	#
	# This method is run within an own thread.
	#
	def __run(self):
		self.__log.notice("Job processing engine started.")

		try:
			while not self.__bTerminate:
				# get a job

				job = self.__jobQueue.getNextWaitingJob()
				if job is None:
					time.sleep(1)
					continue

				# get a job processor for this job

				jobProcessor = self.__jobProcessors.get(job.jobType)
				if jobProcessor is None:
					job.state = EnumJobState.ERR_UNKNOWN
					job.storeProcessingState()
					self.__log.error("No such job processor exists: " + job.jobType)
					continue

				# process the job

				with self.__log.descend("Now processing: " + job.jobID) as log2:
					self.__runJob(job, jobProcessor, log2)
					log2.notice("Job state: " + str(job.state))

					# ----

					if job.state == EnumJobState.SUCCESS:
						# this job is no longer needed.
						log2.notice("Destroying job: " + job.jobID)
						job.destroy()

				# wait for one second

				if self.__bTerminate:
					break
				time.sleep(1)

		finally:
			self.__t = None

		self.__log.notice("Job processing engine terminated.")
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def register(self, p:AbstractJobProcessor, log:jk_logging.AbstractLogger = None):
		if log:
			log.notice("Registering: " + p.__class__.__name__)

		self.__jobProcessors[p.jobType] = p
	#

	@jk_typing.checkFunctionSignature()
	def start(self, jobQueue:JobQueue):
		if self.__t:
			raise Exception("Processing engine is already running!")

		self.__jobQueue = jobQueue
		self.__t = threading.Thread(target = self.__run, daemon=True)
		self.__t.start()
	#

	def terminate(self):
		if not self.__t:
			return

		self.__bTerminate = True
		self.__terminationFlag.terminate()

		self.__t.join()
		self.__t = None
	#

#














