

import json

import jk_json
import jk_typing
from jk_testing import Assert
import jk_prettyprintobj

from thaniya_common.cfg import *









class _Magic(CfgComponent_Magic):

	MAGIC = "my-cfg"
	VERSION = 1
	VALID_VERSIONS = [ 1 ]

#



class _MyCfgV1(AbstractCfgComponent):

	VALID_KEYS = [
		CfgKeyValueDefinition(	key="run",			pyType=str,		nullable=True								),
		CfgKeyValueDefinition(	key="foo",			pyType=int,		nullable=True,		defaultValue=1234		),
	]

	def __init__(self):
		super().__init__()

		self._run = None					# str
		self._foo = None					# int
	#

#






class ExampleCfg(AbstractAppCfg):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self):
		super().__init__(
			_Magic,
			True,
			{
				"mycfg": _MyCfgV1(),
			}
		)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def mycfg(self) -> AbstractCfgComponent:
		return self._groups["mycfg"]
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
	def loadFromFile(filePath:str):
		assert isinstance(filePath, str)

		jData = jk_json.loadFromFile(filePath)

		ret = ExampleCfg()
		ret._loadFromJSON(jData)

		return ret
	#

#










