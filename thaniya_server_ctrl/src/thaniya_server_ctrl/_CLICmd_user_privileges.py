

import os

import jk_utils
import jk_argparsing
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from thaniya_server.usermgr import BackupUser
from thaniya_server.usermgr import BackupUserManager

from .AppRuntimeServerCtrl import AppRuntimeServerCtrl







class _CLICmd_user_privileges(CLICmdBase):

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
		return "user-privileges"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "Show a matrix of users and privileges."
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
		with p.out.section("User Privileges") as out:

			privileges = self.__appRuntime.userMgr.supportedPrivileges
			table = jk_console.SimpleTable()
			table.addRow(
				*([ "USER" ] + privileges)
				).hlineAfterRow = True

			for u in self.__appRuntime.userMgr.users:
				assert isinstance(u, BackupUser)
				rowData = [ u.userName ]
				for privilege in privileges:
					rowData.append("yes" if self.__appRuntime.userMgr.hasPrivilege(u, privilege) else "no")
				table.addRow(*rowData)

			p.out.printTable(table)
	#

#





