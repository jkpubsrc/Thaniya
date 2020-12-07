

import os
import shutil

import jk_utils
import jk_argparsing
import jk_mounting
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from .AppRuntimeServerCtrl import AppRuntimeServerCtrl

from .TextDiskSpaceGraphGenerator import TextDiskSpaceGraphGenerator







class _CLICmd_notify(CLICmdBase):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, appRuntime:AppRuntimeServerCtrl):
		self.__appRuntime = appRuntime
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def cmdName(self) -> str:
		return "notify"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "Send a notification signal to other thaniya processes."
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
		with p.out.section("Send notification signal") as out:

			n = self.__appRuntime.notifyOtherThaniyaProcesses()
			p.log.info("{} Thaniya process(es) notified.".format(n))
	#

#





