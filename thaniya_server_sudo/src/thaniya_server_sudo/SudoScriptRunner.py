




import typing
import re
import os
import subprocess
import sys

import jk_prettyprintobj
import jk_typing
import jk_utils
import jk_logging

from .SudoScriptResult import SudoScriptResult





class SudoScriptRunner(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, scriptDirPath:str):
		assert sys.version_info[0] == 3

		self.__scriptDirPath = scriptDirPath
		self.__scriptNames = set()
		for fe in os.scandir(scriptDirPath):
			if fe.is_file():
				m = re.match("^([a-zA-Z_0-9-]+)\.sh$", fe.name)
				if m is not None:
					self.__scriptNames.add(m.group(1))
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def scriptDirPath(self) -> str:
		return self.__scriptDirPath
	#

	#
	# Returns a list of scripts that can be run as superuser.
	#
	@property
	def scriptNames(self) -> typing.List[str]:
		return sorted(self.__scriptNames)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def run0(self, scriptName:str, stdin:str = None, timeout:float = None) -> SudoScriptResult:

		return self.run(scriptName, [], stdin, timeout)
	#

	@jk_typing.checkFunctionSignature()
	def run0E(self,
			scriptName:str,
			stdin:str = None,
			timeout:float = None,
			exErrMsg:str = None,
			log:jk_logging.AbstractLogger = None
		) -> SudoScriptResult:

		return self.runE(scriptName, [], stdin, timeout, exErrMsg, log)
	#

	@jk_typing.checkFunctionSignature()
	def run1(self, scriptName:str, argument1:str, stdin:str = None, timeout:float = None) -> SudoScriptResult:
		assert argument1

		return self.run(scriptName, [ argument1 ], stdin, timeout)
	#

	@jk_typing.checkFunctionSignature()
	def run1E(self,
			scriptName:str,
			argument1:str,
			stdin:str = None,
			timeout:float = None,
			exErrMsg:str = None,
			log:jk_logging.AbstractLogger = None
		) -> SudoScriptResult:

		assert argument1

		return self.runE(scriptName, [ argument1 ], stdin, timeout, exErrMsg, log)
	#

	@jk_typing.checkFunctionSignature()
	def run2(self, scriptName:str, argument1:str, argument2:str, stdin:str = None, timeout:float = None) -> SudoScriptResult:
		assert argument1
		assert argument2

		return self.run(scriptName, [ argument1, argument2 ], stdin, timeout)
	#

	@jk_typing.checkFunctionSignature()
	def run2E(self,
			scriptName:str,
			argument1:str,
			argument2:str,
			stdin:str = None,
			timeout:float = None,
			exErrMsg:str = None,
			log:jk_logging.AbstractLogger = None
		) -> SudoScriptResult:

		assert argument1
		assert argument2

		return self.runE(scriptName, [ argument1, argument2 ], stdin, timeout, exErrMsg, log)
	#

	@jk_typing.checkFunctionSignature()
	def run3(self, scriptName:str, argument1:str, argument2:str, argument3:str, stdin:str = None, timeout:float = None) -> SudoScriptResult:
		assert argument1
		assert argument2
		assert argument3

		return self.run(scriptName, [ argument1, argument2, argument3 ], stdin, timeout)
	#

	@jk_typing.checkFunctionSignature()
	def run3E(self,
			scriptName:str,
			argument1:str,
			argument2:str,
			argument3:str,
			stdin:str = None,
			timeout:float = None,
			exErrMsg:str = None,
			log:jk_logging.AbstractLogger = None
		) -> SudoScriptResult:

		assert argument1
		assert argument2
		assert argument3

		return self.runE(scriptName, [ argument1, argument2, argument3 ], stdin, timeout, exErrMsg, log)
	#

	#
	# Run the specified script as <c>root</c>.
	# An error result is returend if the script did not run properly.
	#
	# @param		str scriptName		(required) The name of the script to run. An exception is raised if the specified script does not exist.
	# @param		str[] arguments		(required) A list of script arguments. (This may be an empty list, but a list *must* be specified.)
	# @param		str stdin			(optional) Data that should be piped to the script.
	# @param		float timeout		(optional) A timeout value in seconds. If the script has not terminated within the specified time an exception is raised.
	#
	@jk_typing.checkFunctionSignature()
	def run(self, scriptName:str, arguments:list, stdin:str = None, timeout:float = None) -> SudoScriptResult:
		if scriptName not in self.__scriptNames:
			raise Exception("No such script: " + scriptName)

		# ----

		if stdin is None:
			p_stdin = None
			p_input = None

		else:
			p_stdin = subprocess.PIPE
			p_input = stdin

		cmdPath = os.path.join(self.__scriptDirPath, scriptName + ".sh")
		cmdArgs = [
			"/usr/bin/sudo",
			cmdPath,
		]
		cmdArgs.extend(arguments)

		if sys.version_info[1] <= 6:
			p = subprocess.Popen(
				cmdArgs,
				universal_newlines=True,			# in python 3.7 this is replaced by argument named 'text' (which indicates that text input is required)
				shell=False,
				stdin=p_stdin,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
		else:
			raise jk_utils.ImplementationErrorException()

		(stdout, stderr) = p.communicate(input=p_input, timeout=timeout)
		returnCode = p.wait()

		return SudoScriptResult(cmdPath, arguments, stdout, stderr, returnCode)
	#

	#
	# Run the specified script as <c>root</c>.
	# An exception is raised if the script did not run properly.
	#
	# @param		str scriptName		(required) The name of the script to run. An exception is raised if the specified script does not exist.
	# @param		str[] arguments		(required) A list of script arguments. (This may be an empty list, but a list *must* be specified.)
	# @param		str stdin			(optional) Data that should be piped to the script.
	# @param		float timeout		(optional) A timeout value in seconds. If the script has not terminated within the specified time an exception is raised.
	# @param		str exErrMsg		(optional) A text error message to use for the exception if an error occured. If you specify <c>None</c> here a default
	#									error message is generated.
	# @param		AbstractLogger log	(optional) If an error exists and a logger has been specified, debugging data from attempting to run the external
	#									script will be written to this logger.
	@jk_typing.checkFunctionSignature()
	def runE(self,
			scriptName:str,
			arguments:list,
			stdin:str = None,
			timeout:float = None,
			exErrMsg:str = None,
			log:jk_logging.AbstractLogger = None
		) -> SudoScriptResult:

		r = self.run(scriptName, arguments, stdin, timeout)
		if r.isError:
			if log:
				r.dump(printFunc=log.notice)
			if exErrMsg is None:
				if r.errorID:
					exErrMsg = "Error encountered: {}".format(r.errorID)
				else:
					exErrMsg = "Error encountered: (unknown)"
			raise Exception(exErrMsg)

		return r
	#

#
