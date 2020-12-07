



import threading
import typing
import time

import jk_typing
import jk_exceptionhelper

from ._SchedulerJob import _SchedulerJob







class Scheduler(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self):
		self.__jobs = {}
		self.__temp_jobsToRemove = []
		self.__backgroundThread = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __getNextRun(self) -> typing.Union[float,None]:
		if not self.__jobs:
			return None

		return min([ job.tNextRun for job in self.__jobs.values() ])
	#

	def __thread_run_pending(self):
		while bool(self.__backgroundThread):
			try:
				tNext = self.__getNextRun()
				if tNext is None:
					# no job
					time.sleep(5)
					continue

				t = tNext - time.time()
				if t > 0:
					time.sleep(t)

				self.run_pending()
			except Exception as ee:
				print("ERROR:", ee)
				break
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def startBackgroundThread(self):
		if self.__backgroundThread is not None:
			raise Exception("Background thread already started!")

		self.__backgroundThread = threading.Thread(target=self.__thread_run_pending, daemon=True)
		self.__backgroundThread.start()
	#

	def __del__(self):
		self.__backgroundThread = None
	#

	def scheduleRepeat(self, waitSeconds:int, jobCallable, jobArguments:typing.Union[list,tuple] = None, identifier = None):
		if identifier is None:
			identifier = jobCallable
		if not isinstance(identifier, int):
			identifier = id(identifier)

		job = _SchedulerJob(identifier, waitSeconds, False, jobCallable, jobArguments)
		job.tNextRun = time.time() + waitSeconds
		self.__jobs[identifier] = job
	#

	def remove(self, identifier):
		assert identifier is not None
		if not isinstance(identifier, int):
			identifier = id(identifier)

		if identifier in self.__jobs:
			del self.__jobs[identifier]
		else:
			raise Exception("No such job!")
	#

	def clear(self):
		self.__jobs.clear()
	#

	def run_pending(self):
		#print("SCHEDULER: Run pending ...")
		tNow = time.time()

		for job in self.__jobs.values():
			runInSeconds = job.tNextRun - tNow
			if runInSeconds <= 0:
				#print("SCHEDULER: Running: " + str(job))
				try:
					job.run()
				except Exception as ee:
					jk_exceptionhelper.analyseException(ee).dump()

				job.tNextRun = tNow + job.waitSeconds
				if job.bRunOnce:
					self.__temp_jobsToRemove.append(job)

		if self.__temp_jobsToRemove:
			for job in self.__temp_jobsToRemove:
				del self.__jobs[job.identifier]
			self.__temp_jobsToRemove.clear()
	#

#














