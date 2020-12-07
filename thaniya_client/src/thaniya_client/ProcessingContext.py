

import time
import datetime
import typing

import jk_utils
import jk_logging
from jk_typing import checkFunctionSignature

from .ProcessingFallThroughError import ProcessingFallThroughError
from .ThaniyaBackupContext import ThaniyaBackupContext
from .BD2 import BD2





"""
def thaniya_context(description):
	def thaniya_context2(func):
		def wrapped(*wargs, **kwargs):
			print(func)
			print(func.__annotations__)
			kwargs["c"] = "cc"
			return 'I got a wrapped up {} for you'.format(str(func(*wargs, **kwargs)))
		return wrapped
	return thaniya_context2
#
"""




"""
class MeasureDuration(object):

	def __init__(self, taskName:str, log:jk_logging.AbstractLogger):
		self.__taskName = taskName
		self.__log = log

		self.__t0 = None
	#

	def __enter__(self):
		self.__t0 = time.time()
		d0 = datetime.datetime.fromtimestamp(self.__t0)
		self.__log.info("Starting " + self.__taskName + " at: " + str(d0) + " (" + str(int(self.__t0)) + ")")
	#

	def __exit__(self, ex_type, exception, ex_traceback):
		t1 = time.time()
		d1 = datetime.datetime.fromtimestamp(t1)
		self.__log.info("Terminating " + self.__taskName + " at: " + str(d1) + " (" + str(int(t1)) + ")")

		fDurationSeconds = t1 - self.__t0
		self.__log.info("Time spent on " + self.__taskName + ": " + jk_utils.formatTime(fDurationSeconds))
	#

#
"""






#
# This context is similar to ThaniyaBackupContext, but it comprises a major processing step and measures performance.
#
class ProcessingContext(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# @param	str name						The text to write to the log on descend.
	# @param	str targetDirPath				The destination directory to write files to. This argument is <c>None</c> if a specific
	#											section of activities (wrapped by this context) should not perform any writing.
	# @param	bool bMeasureDuration			If <c>True</c> after completing this context time measurement information is written to the log.
	# @param	str statsDurationKey			The name of the variable under which to store the stats data if processing is completed.
	#
	@checkFunctionSignature()
	def __init__(self,
		text:str,
		bd2:BD2,
		bMeasureDuration:bool,
		statsDurationKey:typing.Union[str,None],
		):

		self.__bd2 = bd2
		self.__text = text
		self.__nestedLog = None
		self.__bMeasureDuration = bMeasureDuration
		self.__statsDurationKey = statsDurationKey

		self.__t0 = None
		self.__t1 = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def log(self) -> jk_logging.AbstractLogger:
		return self.__nestedLog
	#

	@property
	def bd2(self) -> BD2:
		return self.__bd2
	#

	#
	# The duration measured from the time when the context is entered.
	#
	@property
	def duration(self) -> float:
		if self.__t0 is None:
			return -1
		else:
			if self.__t1 is None:
				return time.time() - self.__t0
			else:
				return self.__t1 - self.__t0
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __enter__(self):
		self.__nestedLog = self.__bd2.log.descend(self.__text)

		self.__t0 = time.time()
		# d0 = datetime.datetime.fromtimestamp(self.__t0)
		# self.__nestedLog.info("Starting this activity at: " + str(d0) + " (" + str(int(self.__t0)) + ")")

		return ThaniyaBackupContext(self.__bd2, self.__nestedLog)
	#

	def __exit__(self, ex_type, ex_value, ex_traceback):
		self.__t1 = time.time()
		#d1 = datetime.datetime.fromtimestamp(t1)
		fDurationSeconds = self.__t1 - self.__t0

		if ex_type:
			self.__bd2.setErrorFlag()
			if (ex_type != jk_logging.ExceptionInChildContextException) and (ex_type != ProcessingFallThroughError):
				self.__nestedLog.error(ex_value)
				raise ProcessingFallThroughError()

		# NOTE: we skip fall through errors as they already have been logged

		#if exception and (exception is not jk_logging.AbstractLogger._EINSTANCE):
		if ex_value and not isinstance(ex_value, ProcessingFallThroughError) and not ex_type.__name__.endswith("ExceptionInChildContextException"):			# TODO: simplify!
			self.__nestedLog.error(ex_value)

		if self.__bMeasureDuration:
			if ex_value:
				#self.__nestedLog.error("Terminating with error at: " + str(d1) + " (" + str(int(t1)) + ")")
				#self.__nestedLog.error("Time spent: " + jk_utils.formatTime(fDurationSeconds))
				self.__nestedLog.notice("Terminating with error after: " + jk_utils.formatTime(fDurationSeconds))
			else:
				#self.__nestedLog.success("Terminating without error at: " + str(d1) + " (" + str(int(t1)) + ")")
				#self.__nestedLog.success("Time spent: " + jk_utils.formatTime(fDurationSeconds))
				self.__nestedLog.notice("Terminating with success after: " + jk_utils.formatTime(fDurationSeconds))

		if self.__bMeasureDuration:
			if not ex_value:
				if (self.__bd2.statsContainer is not None) and self.__statsDurationKey:
					self.__bd2.statsContainer.setValue(self.__statsDurationKey, fDurationSeconds)

		if ex_value and not isinstance(ex_value, ProcessingFallThroughError) and not ex_value.__class__.__name__.endswith("ExceptionInChildContextException"):			# TODO: simplify!
			raise ProcessingFallThroughError()
	#

#








