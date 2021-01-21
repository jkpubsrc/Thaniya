

import re
import os
import typing
import time
import datetime
import json
import sys
import socket

import jk_typing
import jk_utils
import jk_mounting
import jk_logging
#from jk_testing import Assert
import jk_json

from .ProcessingFallThroughError import ProcessingFallThroughError
from .constants import *
from .ThaniyaIO import ThaniyaIO
from .ILocalBackupOriginInfo import ILocalBackupOriginInfo
from .ThaniyaBackupStats import ThaniyaBackupStats
from .utils.PrivateTempDir import PrivateTempDir
from .tasks.AbstractThaniyaTask import AbstractThaniyaTask
from .ILocalBackupOriginInfo import ILocalBackupOriginInfo
from .ThaniyaClientCfg import ThaniyaClientCfg








#
# This class accompanies the execution of a backup. It provides (and stores) essential information for the current backup.
#
# This class is implemented as a context. The reason is simple: On enter preparational and on exit cleanup tasks are performed automatically.
# These are specifically:
#
# * on construction:
#		* Loading of the client configuration
# * on enter:
#		* Creation of a new private temporary directory (based on the configuration)
#		* Remembering the time stamp (representing the beginning of the backup process)
#		* Creating a logger that a) logs to the main logger specified during construction and b) logs to a buffer that later on can be sent to the server
# * on exit:
#		* Log the exception (if an exception occurred)
#
class BD2(ILocalBackupOriginInfo):

	_EPOCH = datetime.datetime.utcfromtimestamp(0)

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	# @param		str backupIdentifier			This is the identifier the client specifies to categorize his backup. This way the client can perform multiple
	#												individual backups independently from each other for different aspects of a computer system that then as a whole
	#												represents "the backup".
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, cfg:ThaniyaClientCfg, backupIdentifier:str, mainLog:jk_logging.AbstractLogger):
		assert backupIdentifier

		self.__cfg = cfg

		self.__beginDateTime = None
		self.__beginEpochTime = None

		self.__localHostName = socket.gethostname()
		assert isinstance(self.__localHostName, str)

		self.__backupIdentifier = backupIdentifier

		self.__currentUserName = jk_utils.users.lookup_username()	# raises an exception on error
		assert isinstance(self.__currentUserName, str)

		self.__bSimulate = False									# NOTE: I used to use such a flag; I removed that feature, now it is set to <c>True</c> by default;

		self.__statsContainer = None
		self.__privateTempDir = None

		self.__mainLog = mainLog
		self.__blog = None
		self.__log = None

		# this flag indicates if we had an error; this flag is set automatically on error by instances of ProcessingContext.
		self.__bError = False

		# this variable is set by the framework if a) a connector has mounted something and b) if the mounting operation has succeeded.
		self.mountDirPath = None

		# no target dir path (yet); this variable will be assigned at some point in the future
		self.baseTargetDirPath = None

		# no target dir path (yet); this variable will be assigned at some point in the future
		self.effectiveTargetDirPath = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# Returns <c>True</c> if there has been any error, either specified explicitely by setting the flag <c>bError</c> or by writing an error message to the log.
	#
	@property
	def hasError(self) -> bool:
		return self.__bError or self.__dlog.stats.hasAnyError
	#

	@property
	def hasWarning(self) -> bool:
		return self.__dlog.stats.hasWarning
	#

	#
	# The logger to use. Always use *this* logger as it will write log data to all loggers: It will write to the main logger as well as the buffer logger.
	#
	@property
	def log(self) -> jk_logging.AbstractLogger:
		return self.__log
	#

	#
	# This is a buffer logger that stores all log messages. It is provided for you to get access to the stored log messages.
	# For regular logging use <c>log</c> instead.
	#
	@property
	def blog(self) -> jk_logging.BufferLogger:
		return self.__blog
	#

	#
	# Returns the LogStats object that provides statistics about the log messages.
	#
	@property
	def logStats(self) -> jk_logging.LogStats:
		return self.__dlog.stats
	#

	#
	# A private temporary directory that can be used for the duration of the backup process.
	# It get's destroyed automatically after the backup is completed.
	#
	@property
	def privateTempDir(self) -> PrivateTempDir:
		return self.__privateTempDir
	#

	@property
	def statsContainer(self) -> ThaniyaBackupStats:
		return self.__statsContainer
	#

	#
	# Time stamp of the start of this backup.
	#
	@property
	def backupDateTime(self) -> datetime.datetime:
		return self.__beginDateTime
	#

	#
	# Time stamp of the start of this backup in seconds since Epoch.
	#
	@property
	def backupEpochTime(self) -> int:
		return self.__beginEpochTime
	#		

	#
	# The current host name we currently run this backup on.
	#
	@property
	def localHostName(self) -> str:
		return self.__localHostName
	#

	#
	# The current user performing this backup.
	#
	@property
	def currentUserName(self) -> str:
		return self.__currentUserName
	#

	#
	# A string that identifies the type of backup. (There might be a variety of independent backups from different hosts.)
	#
	@property
	def backupIdentifier(self) -> typing.Union[None,str]:
		return self.__backupIdentifier
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __enter__(self):
		self.__statsContainer = ThaniyaBackupStats()

		self.__blog = jk_logging.BufferLogger.create()
		self.__dlog = jk_logging.DetectionLogger.create(self.__blog)
		self.__log = jk_logging.MulticastLogger.create(
			self.__mainLog,
			self.__dlog,
		)
		self.__log.notice("Initializing backup context ...")
		self.__log.notice("tempBaseDir = " + repr(self.__cfg.general.getValue("tempBaseDir")))

		self.__privateTempDir = PrivateTempDir(self.__cfg.general.getValue("tempBaseDir"))
		self.__log.notice("Using private temporary directory: " + str(self.__privateTempDir))

		self.__beginDateTime = datetime.datetime.now()
		self.__beginEpochTime = (self.__beginDateTime - BD2._EPOCH).total_seconds()

		self.__statsContainer.setValue("tStart", self.__beginEpochTime)
		self.__statsContainer.setValue("backupIdentifier", self.__backupIdentifier)
		self.__statsContainer.setValue("backupUserName", self.__currentUserName)
		self.__statsContainer.setValue("hostName", self.__localHostName)
		self.__statsContainer.setValue("simulate", self.__bSimulate)

		return self
	#

	def __exit__(self, ex_type, ex_value, ex_traceback):
		if ex_type:
			self.__bError = True
			if (ex_type != jk_logging.ExceptionInChildContextException) and (ex_type != ProcessingFallThroughError):
				self.__log.error(ex_value)

		self.__log.notice("Cleaning up backup context ...")
		self.__log = None
		self.__blog = None
		self.__beginDateTime = None
		self.__beginEpochTime = None
		self.__statsContainer = None
		if self.__privateTempDir is not None:
			self.__privateTempDir.cleanup()
			self.__privateTempDir = None

		if ex_type:
			raise ProcessingFallThroughError()
	#

	#
	# Invoke this method in order to set the error flag.
	#
	def setErrorFlag(self):
		self.__bError = True
	#

#


















