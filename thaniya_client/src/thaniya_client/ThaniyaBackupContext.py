

import os

import jk_logging
from jk_testing import Assert

from .utils.PrivateTempDir import PrivateTempDir
from .ProcessingFallThroughError import ProcessingFallThroughError







#
# This context provides access to important components and data required to perform backup tasks.
#
class ThaniyaBackupContext(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, bd2, log:jk_logging.AbstractLogger):
		#Assert.isInstance(bd2, "BD2")								# extend Assert to support string class names
		Assert.isInstance(log, jk_logging.AbstractLogger)

		self.__bd2 = bd2
		self.__log = log
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def privateTempDir(self) -> PrivateTempDir:
		return self.__bd2.privateTempDir
	#

	#
	# Returns <c>True</c> if there has been any error, either specified explicitely by setting the flag <c>bError</c> or by writing an error message to the log.
	#
	@property
	def hasError(self) -> bool:
		return self.__bd2.hasError
	#

	"""
	@property
	def duration(self) -> float:
		return self.__processingContext.duration
	#
	"""

	@property
	def log(self) -> jk_logging.AbstractLogger:
		return self.__log
	#

	@property
	def targetDirPath(self) -> str:
		return self.__bd2.effectiveTargetDirPath
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Perform log descending.
	#
	# @param		str text					The text to write to the logs.
	# @return		ThaniyaBackupContext		Returns a new backup context, now filling a different section of the log.
	#
	def descend(self, text:str):
		return ThaniyaBackupContext(self.__bd2, self.__log.descend(text))
	#

	#
	# Get the abolute path of a file relative to the target directory.
	#
	def absPath(self, fileName:str) -> str:
		if os.path.isabs(fileName):
			assert fileName.startswith(self.__bd2.effectiveTargetDirPath + os.path.sep)
			return fileName
		else:
			return os.path.join(self.__bd2.effectiveTargetDirPath, fileName)
	#

	def __enter__(self):
		return self
	#

	def __exit__(self, ex_type, ex_value, ex_traceback):
		if ex_type:
			self.__bd2.setErrorFlag()
			if (ex_type != jk_logging.ExceptionInChildContextException) and (ex_type != ProcessingFallThroughError):
				self.__log.error(ex_value)
				raise ProcessingFallThroughError()
	#

#




