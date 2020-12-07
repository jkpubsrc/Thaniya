

import os
import json

import jk_json
import jk_utils
import jk_typing
import jk_logging

from thaniya_common.cfg import *








class _Magic(CfgComponent_Magic):

	MAGIC = "thaniya-upload-httpd-cfg"
	VERSION = 1
	VALID_VERSIONS = [ 1 ]

#




class _UploadHttpdV1(AbstractCfgComponent):

	VALID_KEYS = [
		CfgKeyValueDefinition(	key="interface",			pyType=str,		nullable=False	),		# the TCP network interface to listen on
		CfgKeyValueDefinition(	key="port",					pyType=int,		nullable=False	),		# the TCP port number to listen on
		CfgKeyValueDefinition(	key="apiAuthTimeout",		pyType=int,		nullable=False	),		# the time in seconds an API client must complete the authentification process
		CfgKeyValueDefinition(	key="apiSessionTimeout",	pyType=int,		nullable=False	),		# the time in seconds after an API session is considered to be outdated
	]

	def __init__(self):
		super().__init__()

		self._interface = None					# str
		self._port = None						# int
		self._apiAuthTimeout = None				# int
		self._apiSessionTimeout = None			# int
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



class _SlotMgrV1(AbstractCfgComponent):

	VALID_KEYS = [
		CfgKeyValueDefinition(	key="stateDir",					pyType=str,						nullable=False																	),
		CfgKeyValueDefinition(	key="securitySpaceMarginBytes",	pyType=jk_utils.AmountOfBytes,	nullable=False,	parserFunc=jk_utils.AmountOfBytes.parseFromStr,	toJSONFunc=str	),
		CfgKeyValueDefinition(	key="resultDir",				pyType=str,						nullable=False																	),
		CfgKeyValueDefinition(	key="logFile",					pyType=str,						nullable=False	),
		CfgKeyValueDefinition(	key="logRollover",				pyType=str,						nullable=False	),
	]

	def __init__(self):
		super().__init__()

		self._stateDir = None							# str
		self._securitySpaceMarginBytes = None			# int
		self._resultDir = None							# str
		self._logFile = None				# str
		self._logRollover = None			# str
	#

#



"""
class _JobProcessingV1(AbstractCfgComponent):

	VALID_KEYS = [
		#CfgKeyValueDefinition(	key="logFile",			pyType=str,		nullable=False	),
		#CfgKeyValueDefinition(	key="logRollover",		pyType=str,		nullable=False	),
		CfgKeyValueDefinition(	key="jobQueueDir",		pyType=str,		nullable=False	),
	]

	def __init__(self):
		super().__init__()

		#self._logFile = None				# str
		#self._logRollover = None			# str
		self._jobQueueDir = None			# str
	#

#
"""





#
# Represents status and statistical information about a backup performed.
#
class UploadHttpdCfg(AbstractAppCfg):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self):
		super().__init__(
			_Magic,
			True,
			{
				"httpd": _UploadHttpdV1(),
				"userMgr": _UserMgrV1(),
				"sudo": _SudoV1(),
				"slotMgr": _SlotMgrV1(),
				#"jobProcessing": _JobProcessingV1(),
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
	def slotMgr(self) -> AbstractCfgComponent:
		return self._groups["slotMgr"]
	#

	#@property
	#def jobProcessing(self) -> AbstractCfgComponent:
	#	return self._groups["jobProcessing"]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	################################################################################################################################
	## Static Methods
	################################################################################################################################

	@staticmethod
	def load():
		cfgFilePath = "/etc/thaniya/cfg-upload-httpd.jsonc"
		if not os.path.isfile(cfgFilePath):
			raise Exception("No such configuration file: " + cfgFilePath)
		return UploadHttpdCfg.loadFromFile(cfgFilePath)
	#

	@staticmethod
	def loadFromFile(filePath:str):
		assert isinstance(filePath, str)

		jData = jk_json.loadFromFile(filePath)

		ret = UploadHttpdCfg()
		ret._loadFromJSON(jData)

		return ret
	#

#









