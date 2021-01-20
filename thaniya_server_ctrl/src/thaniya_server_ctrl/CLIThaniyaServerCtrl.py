#!/usr/bin/python3


__version__ = "0.2019.4.10"



import sys
import os
import typing

import jk_argparsing
import jk_logging

from thaniya_server.app.AbstractCLIApp import AbstractCLIApp

from .AppRuntimeServerCtrl import AppRuntimeServerCtrl

from ._CLICmd_df import _CLICmd_df
from ._CLICmd_processes_list import _CLICmd_processes_list
from ._CLICmd_notify import _CLICmd_notify
from ._CLICmd_user_list import _CLICmd_user_list
from ._CLICmd_user_enable import _CLICmd_user_enable
from ._CLICmd_user_disable import _CLICmd_user_disable
from ._CLICmd_user_create import _CLICmd_user_create
from ._CLICmd_user_setpwd import _CLICmd_user_setpwd
from ._CLICmd_user_delete import _CLICmd_user_delete
from ._CLICmd_user_setuploadpwd import _CLICmd_user_setuploadpwd
from ._CLICmd_user_privileges import _CLICmd_user_privileges
from ._CLICmd_slot_list import _CLICmd_slot_list
from ._CLICmd_slot_reset import _CLICmd_slot_reset
from ._CLICmd_volumes_list import _CLICmd_volumes_list
from ._CLICmd_volume_create_directory import _CLICmd_volume_create_directory
from ._CLICmd_volume_activate import _CLICmd_volume_activate
from ._CLICmd_volume_deactivate import _CLICmd_volume_deactivate










class CLIThaniyaServerCtrl(AbstractCLIApp):

	def __init__(self):
		super().__init__()
	#

	def shortAppDescriptionImpl(self) -> str:
		return "Management tool for Thaniya backup manager."
	#

	def shortAppParamInfoImpl(self) -> str:
		return "[options] <command>"
	#

	def configurationOptionKeysImpl(self) -> typing.List[str]:
		#return [ "repoKeyDir", "buildPkgKeyDir", "repoStorageDir" ]
		return []
	#

	def initializeImpl(self, ap:jk_argparsing.ArgsParser, log:jk_logging.AbstractLogger):
		self.__appRuntime = AppRuntimeServerCtrl(__file__, log)

		ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
		ap.setLicense("apache")

		"""
		ap.createOption(None, "repo-keydir", "Directory for storing repository keys. Some commands require this information. If a configuration exists this value overrides a value specified in the configuration.") \
			.expectDirectory("<dir>", minLength=1, mustExist=True, toAbsolutePath=True) \
			.onOption = lambda argOption, argOptionArguments, parsedArgs: parsedArgs.optionData.set("repoKeyDir", argOptionArguments[0])
		ap.createOption(None, "buildpkg-keydir", "Directory for storing keys used for signing packages. Some commands require this information. If a configuration exists this value overrides a value specified in the configuration.") \
			.expectDirectory("<dir>", minLength=1, mustExist=True, toAbsolutePath=True) \
			.onOption = lambda argOption, argOptionArguments, parsedArgs: parsedArgs.optionData.set("buildPkgKeyDir", argOptionArguments[0])
		ap.createOption(None, "repo-wwwdir", "Directory for storing repository packages to serve to clients. Some commands require this information. If a configuration exists this value overrides a value specified in the configuration.") \
			.expectDirectory("<dir>", minLength=1, mustExist=True, toAbsolutePath=True) \
			.onOption = lambda argOption, argOptionArguments, parsedArgs: parsedArgs.optionData.set("repoStorageDir", argOptionArguments[0])
		"""

		for clazz in [
			_CLICmd_df,
			_CLICmd_processes_list,
			_CLICmd_notify,
			_CLICmd_user_list,
			_CLICmd_user_enable,
			_CLICmd_user_disable,
			_CLICmd_user_create,
			_CLICmd_user_setpwd,
			_CLICmd_user_delete,
			_CLICmd_user_setuploadpwd,
			_CLICmd_user_privileges,
			_CLICmd_slot_list,
			_CLICmd_slot_reset,
			_CLICmd_volumes_list,
			_CLICmd_volume_create_directory,
			_CLICmd_volume_activate,
			_CLICmd_volume_deactivate,
			]:

			self.registerCLICmd(clazz(self.__appRuntime), log)
	#

#



















