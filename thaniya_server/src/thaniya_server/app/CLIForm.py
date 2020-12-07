



import typing

import jk_typing
import jk_paramsassert

from ._IOutputWriter2 import _IOutputWriter2
from ._CLIFormEntry import _CLIFormEntry






class CLIForm(object):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	def __init__(self, w:_IOutputWriter2):
		assert isinstance(w, _IOutputWriter2)
		self.__w = w
		self.__formElements = []
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def maxWidth(self) -> int:
		if self.__formElements:
			return max([ x.maxWidth for x in self.__formElements ])
		else:
			return 0
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def addEntry(self, name:str, label:str, label2:typing.Union[str,None], dtype:typing.Union[type,str], typeParser = None, **kwargs):
		if dtype == "pwd":
			self.__formElements.append(_CLIFormEntry(name, label, None, "pwd", typeParser, jk_paramsassert.ParamDef(name, str, **kwargs)))
		elif dtype == "pwd2":
			self.__formElements.append(_CLIFormEntry(name, label, label2, "pwd2", typeParser, jk_paramsassert.ParamDef(name, str, **kwargs)))
		else:
			self.__formElements.append(_CLIFormEntry(name, label, None, None, typeParser, jk_paramsassert.ParamDef(name, dtype, **kwargs)))
	#

	def _doInput(self, maxWidth:int, outReturnValues:dict) -> bool:
		for formEntry in self.__formElements:
			if not formEntry.doInput(self.__w, maxWidth, outReturnValues):
				#print(">>>1")
				return False

		#print(">>>2")
		return True
	#

	def run(self, maxWidth:int = None) -> typing.Union[dict,None]:
		if maxWidth is not None:
			assert isinstance(maxWidth, int)
		else:
			maxWidth = self.maxWidth

		# ----

		ret = {}

		if not self._doInput(maxWidth, ret):
			#print(">>>3")
			return None

		#print(">>>4", ret)
		return ret
	#

#


















