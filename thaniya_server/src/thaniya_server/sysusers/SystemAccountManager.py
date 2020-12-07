

import re
import typing

import jk_sysinfo
import jk_typing
import jk_json
import jk_logging

from thaniya_server_sudo import SudoScriptResult
from thaniya_server_sudo import SudoScriptRunner

from .SystemAccount import SystemAccount








class SystemAccountManager(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, sudoScriptRunner:SudoScriptRunner):
		self.__sudoScriptRunner = sudoScriptRunner

		self.__accounts = {}

		self.update()
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def accountNames(self) -> typing.List[str]:
		return sorted(self.__accounts.keys())
	#

	@property
	def accounts(self) -> typing.List[SystemAccount]:
		return [ self.__accounts[a] for a in sorted(self.__accounts.keys()) ]
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	#
	# NOTE: This is a replacement for <c>jk_sysinfo.get_user_info</c> which uses <c>sudoScriptRunner</c> to obtain the necessary data from <c>/etc/shadow</c>.
	#
	def __getThaniyaUploadSystemAccounts(self, log:jk_logging.AbstractLogger = None) -> dict:
		# retrieve and parse data from /etc/shadow

		r = self.__sudoScriptRunner.run0E(
				"cat_etc_shadow_thaniya_xx",
				exErrMsg="Error encountered changing the password!",
				log = log,
			)

		_jUsersShadow = jk_sysinfo.parse_user_info_etc_shadow(r.stdOut, r.stdErr, r.returnCode)

		# retrieve and parse data from /etc/passwd

		with open("/etc/passwd", "r") as f:
			stdOutPasswd = f.read()
		stdErrPasswd = ""
		exitCodePasswd = 0

		reAccountNameMatcher = re.compile("^thaniya_([0-9][0-9])$")
		_jUsersPasswd = {}
		for systemAccountName, data in jk_sysinfo.parse_user_info_etc_passwd(stdOutPasswd, stdErrPasswd, exitCodePasswd).items():
			m = reAccountNameMatcher.match(systemAccountName)
			if m:
				_jUsersPasswd[systemAccountName] = data

		# merge data and construct SystemAccount objects

		ret = {}
		for systemAccountName, d in _jUsersShadow.items():
			d.update(_jUsersPasswd[systemAccountName])				# if this failes there's something very wrong with /etc/passwd and /etc/shadow; this should never be the case;
			m = reAccountNameMatcher.match(systemAccountName)		# we know that <c>m</c> is not <c>None</c> as things have worked before.
			ret[systemAccountName] = SystemAccount(self, self.__sudoScriptRunner, d, m.group(1))

		return ret
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# Scan /etc/passwd for backup users.
	# This method is called during construction of this object once.
	#
	def update(self):
		self.__accounts = self.__getThaniyaUploadSystemAccounts()
	#

	@jk_typing.checkFunctionSignature()
	def getE(self, userAccount:str) -> SystemAccount:
		ret = self.__accounts.get(userAccount)
		if ret is None:
			raise Exception("No such account: " + userAccount)
		return ret
	#

	@jk_typing.checkFunctionSignature()
	def get(self, userAccount:str) -> typing.Union[SystemAccount,None]:
		return self.__accounts.get(userAccount)
	#

	def __getitem__(self, userAccount:str) -> typing.Union[SystemAccount,None]:
		return self.__accounts.get(userAccount)
	#

#



#am = SystemAccountManager("backup[0-9]+")
#print(am.accountNames)
#am["backup1"].setPassword("test1")

