

import os

import werkzeug.security

import jk_utils
import jk_argparsing
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from thaniya_server.usermgr import BackupUser
from thaniya_server.usermgr import BackupUserManager

from .AppRuntimeServerCtrl import AppRuntimeServerCtrl







class _CLICmd_user_delete(CLICmdBase):

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
		return "user-delete"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "Delete an existing user."
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
		argCmd.expectString("user", minLength=1)
	#

	def _runImpl(self, p:CLICmdParams) -> bool:
		p.out.autoFlush = True
		with p.out.section("Delete user") as out:

			formUserData = p.out.createForm()
			formUserData.addEntry("confirmation", "Are you sure [y/N]?", None, str, values=[ "Y", "y", "N", "n", "" ])

			textWidth = formUserData.maxWidth

			bChanged = False
			try:

				userName = p.cmdArgs[0]
				user = self.__appRuntime.userMgr.getUser(userName)
				if user is None:
					p.out.print("ERROR: No such user: '{}'".format(userName))
					return

				ret = formUserData.run(textWidth)
				if ret is None:
					return
				if ret["confirmation"] not in [ "Y", "y", ]:
					return

				self.__appRuntime.userMgr.deleteUser(userName)
				bChanged = True

				for user in self.__appRuntime.userMgr.users:
					if user.supervises:
						if userName in user.supervises:
							user.supervises.remove(userName)
							user.store()

			finally:
				p.out.print()
				if bChanged:
					p.out.print("User deleted.")
				else:
					p.out.print("No change.")
				p.out.print()
	#

#





