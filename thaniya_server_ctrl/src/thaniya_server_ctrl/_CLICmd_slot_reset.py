

import os

import jk_utils
import jk_argparsing
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from thaniya_server_upload.slots import UploadSlot
from thaniya_server_upload.slots import UploadSlotManager

from .AppRuntimeServerCtrl import AppRuntimeServerCtrl






class _CLICmd_slot_reset(CLICmdBase):

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
		return "slot-reset"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "Reset a backup upload slot. (sudo)"
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
		argCmd.expectString("slot", minLength=1)
	#

	def _runImpl(self, p:CLICmdParams) -> bool:
		with p.out.section("Resetting a backup upload slot") as out:

			bChanged = False
			try:

				slotSystemUserName = p.cmdArgs[0]

				slot = self.__appRuntime.uploadSlotMgr.getSlot(slotSystemUserName)
				if slot is None:
					p.out.print("ERROR: No such slot: '{}'".format(slotSystemUserName))
					return

				slot.reset()
				bChanged = True

			finally:
				p.out.print()
				if bChanged:
					p.out.print("Slot resetted.")
				else:
					p.out.print("No change.")
				p.out.print()
	#

#





