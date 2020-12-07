

import os

import jk_utils
import jk_argparsing
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from thaniya_server_upload.slots import UploadSlot
from thaniya_server_upload.slots import UploadSlotManager

from .AppRuntimeServerCtrl import AppRuntimeServerCtrl






class _CLICmd_slot_list(CLICmdBase):

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
		return "slot-list"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "List all backup upload slots. (sudo)"
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
		with p.out.section("List backup upload slots") as out:

			table = jk_console.SimpleTable()
			table.addRow(
				"systemAccountName",
				"state",
				"backupUser",
				"isAllocated",
				"isInUseByClient",
				"allocationTime",
				"lastUsedTime",
				"completionTime",
				).hlineAfterRow = True

			for slot in sorted(self.__appRuntime.uploadSlotMgr.slots, key=lambda x: x.systemAccountName):
				assert isinstance(slot, UploadSlot)
				table.addRow(
					slot.systemAccountName,
					str(slot.state),
					slot.backupUser.name if slot.backupUser else "-",
					"yes" if slot.isAllocated else "no",
					"yes" if slot.isInUseByClient else "no",
					str(slot.allocationTime) if slot.allocationTime else "-",
					str(slot.lastUsedByClientTime) if slot.lastUsedByClientTime else "-",
					str(slot.completionTime) if slot.completionTime else "-",
				)

			p.out.printTable(table)

	#

#





