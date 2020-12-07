


import random
import subprocess
import grp
import typing

import jk_typing
import jk_prettyprintobj
import jk_json
import jk_logging

from thaniya_server_sudo import SudoScriptRunner
from thaniya_server_sudo import SudoScriptResult









class SystemAccount(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, parent, sudoScriptRunner:SudoScriptRunner, accountInfo:dict, thaniyaUserNo:str):
		self.__parent = parent

		self.__sudoScriptRunner = sudoScriptRunner

		self.__groupID = accountInfo["groupID"]
		self.__groupName = grp.getgrgid(self.__groupID).gr_name
		self.__homeDir = accountInfo["homeDir"]
		assert self.__homeDir
		self.__userID = accountInfo["userID"]
		self.__userName = accountInfo["user"]
		self.__thaniyaUserNo = thaniyaUserNo
		self.__hasPassword = accountInfo["hasPassword"]
		self.__isDisabled = accountInfo["isDisabled"]
		self.__shell = accountInfo["shell"]
		assert self.__shell
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def hasShell(self) -> bool:
		if self.__shell is None:
			# shell has '/usr/bin/nologin'
			return False
		if self.__shell.endswith("/nologin"):
			return False
		if self.__shell.endswith("/false"):
			return False
		return True
	#

	@property
	def thaniyaUserNo(self) -> str:
		return self.__thaniyaUserNo
	#

	@property
	def groupID(self) -> int:
		return self.__groupID
	#

	@property
	def userName(self) -> str:
		return self.__userName
	#

	@property
	def groupName(self) -> str:
		return self.__groupName
	#

	@property
	def homeDir(self) -> str:
		return self.__homeDir
	#

	@property
	def userID(self) -> int:
		return self.__userID
	#

	@property
	def systemAccountName(self) -> int:
		return self.__userName
	#

	@property
	def isDisabled(self) -> bool:
		return self.__isDisabled
	#

	@property
	def isEnabled(self) -> bool:
		return not self.__isDisabled
	#

	@property
	def hasPassword(self) -> bool:
		return self.__hasPassword
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"userName",
			"userID",
			"groupName",
			"groupID",
			"thaniyaUserNo",
			"hasPassword",
			"isDisabled",
			"hasShell",
			"homeDir",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def setPassword(self, password:str, log:jk_logging.AbstractLogger = None):
		assert password
		assert password.strip() == password

		r = self.__sudoScriptRunner.run1E(
			scriptName = "account_chpwd",
			argument1 = self.__thaniyaUserNo,
			stdin = self.__userName + ":" + password + "\n",
			exErrMsg = "Error encountered changing the password!",
			log = log,
		)

		self.__hasPassword = True
		self.__isDisabled = False
	#

	@jk_typing.checkFunctionSignature()
	def setRandomPassword(self, length:int = 32):
		assert isinstance(length, int)
		assert length > 4

		RESERVOIR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		password = "".join(random.SystemRandom().choice(RESERVOIR) for _ in range(0, length))

		self.setPassword(password)

		return password
	#

	def disable(self, log:jk_logging.AbstractLogger = None):
		if not self.__hasPassword:
			raise Exception("Account can not be disabled. It has no password.")

		if not self.__isDisabled:
			r = self.__sudoScriptRunner.run1E(
				scriptName = "account_lock",
				argument1 = self.__thaniyaUserNo,
				exErrMsg = "Error encountered disabling the user account!",
				log = log,
			)

			self.__isDisabled = True
	#

	def enable(self, log:jk_logging.AbstractLogger = None):
		if not self.__hasPassword:
			raise Exception("Account can not be enabled as it has no password.")

		if self.__isDisabled:
			r = self.__sudoScriptRunner.run1E(
				scriptName = "account_unlock",
				argument1 = self.__thaniyaUserNo,
				exErrMsg = "Unknown error encountered enabling the user account!",
				log = log,
			)

			self.__isDisabled = False
	#

	def __eq__(self, other):
		if isinstance(other, SystemAccount):
			return other.__userID == self.__userID
		else:
			return False
	#

	def __ne__(self, other):
		if isinstance(other, SystemAccount):
			return other.__userID != self.__userID
		else:
			return True
	#

	def __lt__(self, other):
		return other.__userName < self.__userName
	#

	def __le__(self, other):
		return other.__userName <= self.__userName
	#

	def __gt__(self, other):
		return other.__userName > self.__userName
	#

	def __ge__(self, other):
		return other.__userName >= self.__userName
	#

#






