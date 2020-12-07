

import os
import json

import jk_json
import jk_typing

from thaniya_common.cfg import *









class _Magic(CfgComponent_Magic):

	MAGIC = "thaniya-archive-httpd-cfg"
	VERSION = 1
	VALID_VERSIONS = [ 1 ]

#



class _ArchiveHttpdV1(AbstractCfgComponent):

	VALID_KEYS = [
		CfgKeyValueDefinition(	key="interface",			pyType=str,		nullable=False	),
		CfgKeyValueDefinition(	key="port",					pyType=int,		nullable=False	),
	]

	def __init__(self):
		super().__init__()

		self._interface = None				# str
		self._port = None					# int
	#

#



class _UserMgrV1(AbstractCfgComponent):

	VALID_KEYS = [
		CfgKeyValueDefinition(	key="usersDir",				pyType=str,		nullable=False	),
	]

	def __init__(self):
		super().__init__()

		self._usersDir = None				# str
	#

#



class _SudoV1(AbstractCfgComponent):

	VALID_KEYS = [
		CfgKeyValueDefinition(	key="scriptsDir",			pyType=str,		nullable=False	),
	]

	def __init__(self):
		super().__init__()

		self._scriptsDir = None				# str
	#

#



class _VolumeMgrV1(AbstractCfgComponent):

	VALID_KEYS = [
		CfgKeyValueDefinition(	key="staticVolumeCfgDir",	pyType=str,		nullable=False	),
		CfgKeyValueDefinition(	key="stateDir",				pyType=str,		nullable=False	),
	]

	def __init__(self):
		super().__init__()

		self._staticVolumeCfgDir = None		# str
		self._stateDir = None				# str
	#

#



class _JobProcessingV1(AbstractCfgComponent):

	VALID_KEYS = [
		CfgKeyValueDefinition(	key="logFile",				pyType=str,		nullable=False	),
		CfgKeyValueDefinition(	key="jobQueueDir",			pyType=str,		nullable=False	),
		CfgKeyValueDefinition(	key="logRollover",			pyType=str,		nullable=False	),
		CfgKeyValueDefinition(	key="incomingBackupsDir",	pyType=str,		nullable=False	),
	]

	def __init__(self):
		super().__init__()

		self._logFile = None				# str
		self._jobQueueDir = None			# str
		self._logRollover = None			# str
		self._incomingBackupsDir = None		# str
	#

#






class ArchiveHttpdCfg(AbstractAppCfg):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self):
		super().__init__(
			_Magic,
			True,
			{
				"httpd": _ArchiveHttpdV1(),
				"userMgr": _UserMgrV1(),
				"sudo": _SudoV1(),
				"volumeMgr": _VolumeMgrV1(),
				"jobProcessing": _JobProcessingV1(),
			}
		)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def httpd(self) -> AbstractCfgComponent:
		return self._groups["httpd"]
	#

	@property
	def userMgr(self) -> AbstractCfgComponent:
		return self._groups["userMgr"]
	#

	@property
	def sudo(self) -> AbstractCfgComponent:
		return self._groups["sudo"]
	#

	@property
	def volumeMgr(self) -> AbstractCfgComponent:
		return self._groups["volumeMgr"]
	#

	@property
	def jobProcessing(self) -> AbstractCfgComponent:
		return self._groups["jobProcessing"]
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
		cfgFilePath = "/etc/thaniya/cfg-archive-httpd.jsonc"
		if not os.path.isfile(cfgFilePath):
			raise Exception("No such configuration file: " + cfgFilePath)
		return ArchiveHttpdCfg.loadFromFile(cfgFilePath)
	#

	@staticmethod
	def loadFromFile(filePath:str):
		assert isinstance(filePath, str)

		jData = jk_json.loadFromFile(filePath)

		ret = ArchiveHttpdCfg()
		ret._loadFromJSON(jData)

		return ret
	#

#










