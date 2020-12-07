

import os

import jk_typing
import jk_logging

from .cfg import AbstractAppCfg
from .utils import IOContext








#
# Base class for application runtime objects.
#
class AppRuntimeBase(object):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	#
	# @param		jk_logging.AbstractLogger log			A log object for informational and error output
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, mainFilePath:str, log:jk_logging.AbstractLogger):
		mainFilePath = os.path.abspath(mainFilePath)
		self.__appBaseDirPath = os.path.dirname(mainFilePath)

		self.__ioCtx = IOContext()

		self.__log = log
		with log.descend("Loading configuration ...") as log2:
			self.__cfg = self._loadConfigurationCallback(log2)
			assert isinstance(self.__cfg, AbstractAppCfg)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def ioCtx(self) -> IOContext:
		return self.__ioCtx
	#

	@property
	def appBaseDirPath(self) -> str:
		return self.__appBaseDirPath
	#

	@property
	def cfg(self) -> AbstractAppCfg:
		return self.__cfg
	#

	@property
	def log(self) -> jk_logging.AbstractLogger:
		return self.__log
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# This method is invoked to automatically load the configuration.
	#
	def _loadConfigurationCallback(self, log:jk_logging.AbstractLogger) -> AbstractAppCfg:
		raise NotImplementedError()
	#

#

















