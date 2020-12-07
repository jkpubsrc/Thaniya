

import os

import jk_utils
import jk_argparsing
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from thaniya_server.usermgr import BackupUser
from thaniya_server.usermgr import BackupUserManager

from .AppRuntimeServerCtrl import AppRuntimeServerCtrl







class _CLICmd_user_list(CLICmdBase):

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
		return "user-list"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "List the existing users."
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
		with p.out.section("Users") as out:

			table = jk_console.SimpleTable()
			table.addRow(
				"Login",
				"EMail",
				"Role",
				"Enabled",
				"CanUpload",
				"Comment",
				).hlineAfterRow = True

			for user in self.__appRuntime.userMgr.users:
				assert isinstance(user, BackupUser)
				table.addRow(
					user.userName,
					user.eMail if user.eMail else "-",
					user.role,
					"yes" if user.enabled else "no",
					"yes" if user.canUpload else "no",
					user.comment if user.comment else "-",
				)

			p.out.printTable(table)
	#

#





