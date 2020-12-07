



import re
import os
import typing

import jk_typing
import jk_json
import jk_prettyprintobj










class SudoScriptResult(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, cmd:str, cmdArgs:typing.List[str], stdout:str, stderr:str, returnCode:int):
		self.__cmd = cmd
		self.__cmdArgs = cmdArgs
		self.__returnCode = returnCode
		self.__errorID = None

		stdOutLines = stdout.split("\n")
		while (len(stdOutLines) > 0) and (len(stdOutLines[-1]) == 0):
			del stdOutLines[-1]
		self.__stdOutLines = stdOutLines

		stdErrLines = stderr.split("\n")
		while (len(stdErrLines) > 0) and (len(stdErrLines[-1]) == 0):
			del stdErrLines[-1]
		self.__stdErrLines = stdErrLines

		if returnCode != 0:
			if stdOutLines:
				m = re.match("^ERR:\s+(err[a-zA-Z0-9]+)$", stdOutLines[0])
				if m:
					self.__errorID = m.group(1)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	#
	# If there was an error this property returns the error code.
	#
	@property
	def errorID(self) -> typing.Union[str,None]:
		return self.__errorID
	#

	#
	# Returns the path used for invoking the command.
	#
	# @return		string			The file path.
	#
	@property
	def commandPath(self) -> str:
		return self.__cmd
	#

	#
	# Returns the arguments used for invoking the command.
	# @return		string[]		The list of arguments (possibly an empty list or <c>None</c>).
	#
	@property
	def commandArguments(self) -> typing.List[str]:
		return self.__cmdArgs
	#

	#
	# The return code of the command after completion.
	#
	# @return		int			The return code.
	#
	@property
	def returnCode(self) -> int:
		return self.__returnCode
	#

	@property
	def stdOut(self) -> str:
		return "\n".join(self.__stdOutLines)
	#

	#
	# The STDOUT output of the command.
	#
	# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdOutLines(self) -> typing.List[str]:
		return self.__stdOutLines
	#

	@property
	def stdErr(self) -> str:
		return "\n".join(self.__stdErrLines)
	#

	#
	# The STDERR output of the command.
	# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdErrLines(self) -> list:
		return self.__stdErrLines
	#

	#
	# Returns <c>True</c> if there was an error.
	# See the sudo script specification for details.
	#
	@property
	def isError(self) -> bool:
		return self.__returnCode != 0
	#

	@property
	def isSuccess(self) -> bool:
		return self.__returnCode == 0
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"commandPath",
			"commandArguments",
			"returnCode",
			"isSuccess",
			"isError",
			"errorID",
			"stdOutLines",
			"stdErrLines",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Return the text data as a regular JSON object.
	#
	def getStdOutAsJSON(self):
		lines = '\n'.join(self.__stdOutLines)
		return jk_json.loads(lines)
	#

	#
	# Returns a dictionary containing all data.
	#
	# @return		dict			Returns a dictionary with data registered at the following keys:
	#								"cmd", "cmdArgs", "stdOut", "stdErr", "retCode", "errID"
	#
	def toJSON(self):
		return {
			"cmd": self.__cmd,
			"cmdArgs" : self.__cmdArgs,
			"stdOut" : self.__stdOutLines,
			"stdErr" : self.__stdErrLines,
			"retCode" : self.__returnCode,
			"errID" : self.__errorID,
		}
	#

#










