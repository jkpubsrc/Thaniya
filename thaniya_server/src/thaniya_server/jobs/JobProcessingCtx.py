


import os
import typing

import jk_typing
import jk_utils
import jk_logging

from .EnumJobState import EnumJobState
from .Job import Job









class JobProcessingCtx(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	# @param		str jobType			The type of the job this job processor can handle.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, terminationFlag:jk_utils.TerminationFlag, log:jk_logging.AbstractLogger, **kwargs):
		assert "terminate" not in kwargs
		assert "checkForTermination" not in kwargs
		assert "log" not in kwargs
		assert "terminationFlag" not in kwargs

		self.__data = kwargs
		self.__log = log
		self.__terminationFlag = terminationFlag
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def log(self) -> jk_logging.AbstractLogger:
		return self.__log
	#

	@property
	def terminationFlag(self) -> jk_utils.TerminationFlag:
		return self.__terminationFlag
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __getattr__(self, name:str):
		if name in self.__data:
			return self.__data[name]
		else:
			return super().__getattr__(name)
	#

	def terminate(self):
		self.__terminationFlag.terminate()
	#

	#
	# Check if the current activity is to be interrupted. In that case an InterruptedException is raised.
	#
	def checkForTermination(self):
		self.__terminationFlag.check()
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#















