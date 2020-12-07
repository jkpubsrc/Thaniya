

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







class _CLICmd_user_create(CLICmdBase):

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
		return "user-create"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "Create a new user."
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
		p.out.autoFlush = True
		with p.out.section("Create a new user") as out:

			formUserName = p.out.createForm()
			formUserName.addEntry("userName", "The login name of the new user:", None, str, minLength=1)

			formUserData = p.out.createForm()
			formUserData.addEntry("eMail", "The email address of the new user (optional):", None, str)
			formUserData.addEntry("comment", "Enter a short description (optional):", None, str)
			formUserData.addEntry("enabled", "Is the user enabled [Y/n]?", None, str, values=[ "Y", "y", "N", "n", "" ])
			formUserData.addEntry("pwd", "The user's login password:", "The user's login password again:", "pwd2", minLength=3)

			textWidth = max(formUserName.maxWidth, formUserData.maxWidth)

			bChanged = False
			try:

				while True:
					ret = formUserName.run(textWidth)
					if ret is None:
						return
					
					userName = ret["userName"]
					user = self.__appRuntime.userMgr.getUser(userName)
					if user is not None:
						p.out.print("ERROR: A user named '{}' already exists!".format(userName))
						continue

					break

				ret2 = formUserData.run(textWidth)

				user = self.__appRuntime.userMgr.createUser(
					userName = userName,
					passwordHash = werkzeug.security.generate_password_hash(ret2["pwd"], method="sha256"),
					eMail = ret2["eMail"] if ret2["eMail"] else None,
					role = "backup",
					comment = ret2["comment"] if ret2["comment"] else None,
					enabled = ret2["enabled"] in [ "Y", "y", "" ],
				)
				assert user is not None

				bChanged = True

				p.out.print()				# TODO: Why does this print statement doesn't create an empty line????
											#		Guess: The last print before the interactive output resulted in an empty line
											#		and the interactive output did not change that state!
				#p.out.print("Please note that no upload password has been set. You have to set this separately using 'users-setuploadpwd'.")
				p.out.print("Please note that no upload password has been set. The user has to set this separately by editing his/her user profile.")

			finally:
				p.out.print()
				if bChanged:
					p.out.print("User created.")
				else:
					p.out.print("No change.")
				p.out.print()
	#

#





