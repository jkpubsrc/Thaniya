

import typing
import string
import random
import os

import jk_utils


from .ThaniyaBackupContext import ThaniyaBackupContext





#
# This class represents an upload channel to a backup repository. Typically this is a client for a backup server.
# To use this class follow the work flow as specified:
# * instantiate a subclass of this class and pass it on to the backup driver;
# * the backup driver invokes `initialize()`; this method should connect to a backup server and prepare everything for backup
# * the backup is performed by writing to the directory returned by `targetDirPath`;
# * the backup driver invokes `deinitialize()` in order to tear down the connection;
#
class AbstractBackupConnector(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def needsToBeRoot(self) -> bool:
		return False
	#

	#
	# This property returns <c>True</c> if this backup connector mounts and unmounts some kind of network drive.
	#
	@property
	def performsMountUnmount(self) -> bool:
		return False
	#

	#
	# Returns <c>True</c> if the backup connector is perperly initialized and everything is now ready for performing a backup.
	#
	@property
	def isReady(self) -> bool:
		raise NotImplementedError()
	#

	#
	# This property returns the target dir path backup data can be uploaded to.
	#
	@property
	def mountDirPath(self) -> str:
		return None
	#

	@property
	def baseTargetDirPath2(self) -> str:
		s = self.baseTargetDirPath
		if s.endswith("/"):
			return s
		else:
			return s + "/"
	#

	@property
	def baseTargetDirPath(self) -> str:
		return None
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def dump(self):
		raise NotImplementedError()
	#

	#
	# @param			ThaniyaBackupContext ctx			The backup context with essential data for performing backup.
	#
	def initialize(self, ctx:ThaniyaBackupContext, nExpectedNumberOfBytesToWrite:int, parameters:dict):
		raise NotImplementedError()
	#

	def deinitialize(self, ctx:ThaniyaBackupContext):
		raise NotImplementedError()
	#

#













