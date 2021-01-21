

import os
import json

import jk_utils
import jk_json
import jk_typing

from thaniya_common.cfg import *









class _Magic(CfgComponent_Magic):

	MAGIC = "thaniya-client-cfg"
	VERSION = 1
	VALID_VERSIONS = [ 1 ]

#



class _ServerV1(AbstractCfgComponent):

	VALID_KEYS = [
		CfgKeyValueDefinition(	key="host",					pyType=str,		nullable=False	),
		CfgKeyValueDefinition(	key="port",					pyType=int,		nullable=False	),
		CfgKeyValueDefinition(	key="login",				pyType=str,		nullable=False	),
		CfgKeyValueDefinition(	key="apiPassword",			pyType=str,		nullable=False	),
	]

	def __init__(self):
		super().__init__()

		self._host = None					# str
		self._port = None					# int
		self._login = None					# str
		self._apiPassword = None			# str
	#

#






class ThaniyaClientCfg(AbstractAppCfg):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self):
		super().__init__(
			_Magic,
			False,
			{
				"server": _ServerV1(),
			}
		)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def server(self) -> AbstractCfgComponent:
		return self._groups["server"]
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	@staticmethod
	def load():
		cfgFilePathCandidates = [
			os.path.join(jk_utils.users.getUserHome(), ".config/thaniya/cfg-client.jsonc"),
			"/etc/thaniya/cfg-client.jsonc",
		]
		for cfgFilePath in cfgFilePathCandidates:
			if os.path.isfile(cfgFilePath):
				return ThaniyaClientCfg.loadFromFile(cfgFilePath)
		raise Exception("No configuration file found!")
	#

	@staticmethod
	def loadFromFile(filePath:str):
		assert isinstance(filePath, str)

		jData = jk_json.loadFromFile(filePath)

		ret = ThaniyaClientCfg()
		ret._loadFromJSON(jData)

		return ret
	#

	#
	# Write the this configuration to the local configuration file at "~/.config/thaniya/cfg-client.jsonc".
	# This method sets file and directory mode to "private" mode: Only the current user will have access!
	#
	# @return		str			The path of the configuration file written.
	#
	def writeToLocal(self, bForceWrite:bool = False) -> str:
		cfgFilePath = os.path.join(jk_utils.users.getUserHome(), ".config/thaniya/cfg-client.jsonc")
		if os.path.isfile(cfgFilePath):
			if not bForceWrite:
				raise Exception("Configuration file already exists and 'bForceWrite' was not specified: " + cfgFilePath)

		iDirMode = jk_utils.ChModValue(userR=True, userW=True, userX=True).toInt()
		iFileMode = jk_utils.ChModValue(userR=True, userW=True).toInt()

		dirPath = os.path.dirname(cfgFilePath)
		os.makedirs(dirPath, iDirMode, exist_ok=True)
		os.chmod(dirPath, iDirMode)

		jk_json.saveToFilePretty(self.toJSON(), cfgFilePath)
		os.chmod(cfgFilePath, iFileMode)

		return cfgFilePath
	#

#










