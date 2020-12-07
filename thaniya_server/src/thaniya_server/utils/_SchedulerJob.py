



import typing

import jk_typing






class _SchedulerJob(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, identifier, waitSeconds:int, bRunOnce:bool, jobCallable, jobArguments:typing.Union[list,tuple] = None):
		assert identifier is not None
		assert waitSeconds > 0
		assert callable(jobCallable)
		if jobArguments is None:
			jobArguments = ()

		# ----

		self.identifier = identifier
		self.bRunOnce = bRunOnce
		self.waitSeconds = waitSeconds
		self.jobCallable = jobCallable
		self.jobArguments = jobArguments

		self.tNextRun = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def run(self):
		self.jobCallable(*self.jobArguments)
	#

#














