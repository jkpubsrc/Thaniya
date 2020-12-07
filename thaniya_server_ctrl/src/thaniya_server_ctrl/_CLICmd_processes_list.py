

import os
import shutil

import jk_utils
import jk_argparsing
import jk_mounting
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from thaniya_server.utils.ProcessFilter import ProcessFilter

from .AppRuntimeServerCtrl import AppRuntimeServerCtrl

FG = jk_console.Console.ForeGround






class _CLICmd_processes_list(CLICmdBase):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, appRuntime:AppRuntimeServerCtrl):
		self.__appRuntime = appRuntime

		#self.__thaniyaUserName = "thaniya"			# jk_utils.users.lookup_username()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def cmdName(self) -> str:
		return "proc-ls"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "List all running backup processes."
	#

	@property
	def usesOutputWriter(self) -> bool:
		return True
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def registerCmd(self, ap:jk_argparsing.ArgsParser) -> jk_argparsing.ArgCommand:
		argCmd = super().registerCmd(ap)
	#

	def _runImpl(self, p:CLICmdParams) -> bool:
		with p.out.section("List processes") as out:

			table = jk_console.SimpleTable()
			table.addRow(
				"pid",
				"user",
				"group",
				"cwd",
				"cmd",
				"args",
				).hlineAfterRow = True

			# list all archive HTTP services
			for jDict in self.__appRuntime.processFilter_thaniyaArchiveHttpd.findProcessStructs():
				table.addRow(
					jDict["pid"],
					jDict["user"],
					jDict["group"],
					jDict["cwd"] if "cwd" in jDict else "",
					jDict["cmd"],
					jDict["args"] if "args" in jDict else "",
				)

			# list all secure file transfers
			for jDict in self.__appRuntime.processFilter_thaniyaSFTPSessions.findProcessStructs():
				table.addRow(
					jDict["pid"],
					jDict["user"],
					jDict["group"],
					jDict["cwd"] if "cwd" in jDict else "",
					jDict["cmd"],
					jDict["args"] if "args" in jDict else "",
				)

			if table.numberOfRows == 1:
				p.out.print("No processes found.")
			else:
				p.out.printTable(table)
	#

#





