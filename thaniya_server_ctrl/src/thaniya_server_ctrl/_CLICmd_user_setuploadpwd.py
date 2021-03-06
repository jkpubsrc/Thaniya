

import os

import jk_utils
import jk_argparsing
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from thaniya_server.usermgr import BackupUser
from thaniya_server.usermgr import BackupUserManager
from thaniya_common.utils import APIPassword

from .AppRuntimeServerCtrl import AppRuntimeServerCtrl







class _CLICmd_user_setuploadpwd(CLICmdBase):

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
		return "user-setuploadpwd"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "Generate a backup upload password for an existing backup user."
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
		with p.out.section("Generate upload password") as out:

			bChanged = False
			try:

				userName = p.cmdArgs[0]
				user = self.__appRuntime.userMgr.getUser(userName)
				if user is None:
					p.out.print("ERROR: No such user: '{}'".format(userName))
					return

				user.uploadPwd = APIPassword.generate()
				user.store()

				bChanged = True

				p.out.print("The following upload password has been set:")
				p.out.print("\t" + user.uploadPwd.toBase64Str())

			finally:
				p.out.print()
				if bChanged:
					p.out.print("Password set.")
				else:
					p.out.print("No change.")
				p.out.print()
	#

#





