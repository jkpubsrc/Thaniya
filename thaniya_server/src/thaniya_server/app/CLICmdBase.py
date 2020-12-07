# NOTE: This is a copy from ~/DevPriv/PythonProjects/MediaWikiMgmt/jk_mediawikirepo/src/jk_mediawikirepo/app/*


import os
import typing

import jk_argparsing
import jk_logging
import jk_typing

from .OutputWriter import OutputWriter
from .CLICmdParams import CLICmdParams






class CLICmdBase(object):

	################################################################################################################################
	## Constructor Methods
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# The type name of this command, such as "scan" or "create".
	#
	# Overwrite this property!
	#
	@property
	def cmdName(self) -> str:
		raise NotImplementedError()
	#

	#
	# The short description.
	#
	# Overwrite this property!
	#
	@property
	def shortDescription(self) -> str:
		raise NotImplementedError()
	#

	#
	# Overwrite this property!
	#
	@property
	def usesOutputWriter(self) -> bool:
		return False
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def registerCmd(self, ap:jk_argparsing.ArgsParser) -> jk_argparsing.ArgCommand:
		return ap.createCommand(self.cmdName, self.shortDescription)
	#

	def checkConfiguration(self, cfg:dict, errorFunc) -> bool:
		return True
	#

	#
	# Execute a command.
	#
	# @param	CLICmdParams dp			(required) The context for the command execution.
	#
	@jk_typing.checkFunctionSignature()
	def run(self, p:CLICmdParams, mainLog:jk_logging.AbstractLogger) -> bool:
		# sanity checks

		#if self.requiresPackageGroupInfo == EnumRequired.REQUIRED:
		#	if dp.pgi is None:
		#		raise Exception("Command \"" + self.cmdName + "\" requires a provided project group information data structure!")
		#if self.requiresPackageInfo == EnumRequired.REQUIRED:
		#	if dp.pi is None:
		#		raise Exception("Command \"" + self.cmdName + "\" requires a provided project information data structure!")

		# run the command

		bSuccess = False
		with mainLog.descend("Executing \"" + self.cmdName + "\" (" + self.shortDescription + ")") as log:
			if p.bSimulate:
				log.warn("Simulation mode is activated.")

			if p.bForceAction:
				log.warn("Enforcing action is activated.")

			if not self.checkConfiguration(p.cfg, log.error):
				raise Exception("Configuration rejected.")

			p.log = log

			if self.usesOutputWriter:
				with OutputWriter() as w:
					p.out = w
					b = self._runImpl(p)
			else:
				b = self._runImpl(p)

			bSuccess = True
			if (b is not None) and isinstance(b, bool):
				bSuccess = b
			log.info("Done." if ((b is None) or b) else "Done (with errors).")

		return bSuccess
	#

	def _runImpl(self, p:CLICmdParams) -> bool:
		raise NotImplementedError()
	#

#






