


import typing

import jk_paramsassert
import jk_typing

from ._IOutputWriter2 import _IOutputWriter2







class _CLIFormEntry(object):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, name:str, label:str, label2:typing.Union[str,None], uiAction:typing.Union[str,None], typeParser, paramDef:jk_paramsassert.ParamDef):
		if typeParser is not None:
			assert callable(typeParser)

		self.uiAction = uiAction
		self.typeParser = typeParser
		self.name = name
		self.label = label
		self.label2 = label2
		self.paramDef = paramDef
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def maxWidth(self) -> int:
		if self.uiAction == "pwd2":
			return max(len(self.label), len(self.label2))
		else:
			return len(self.label)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __doInputStd(self, w:_IOutputWriter2, label:str, width:int) -> tuple:
		s = (width - len(label)) * " " + label + " "
		while True:
			try:
				v = w.inputStd(s)
			except KeyboardInterrupt as ee:
				return False, None

			try:
				v = self.check(v)
				return True, v
			except Exception as ee:
				print("ERROR: " + str(ee))
	#

	def __doInputPwd(self, w:_IOutputWriter2, label:str, width:int) -> tuple:
		s = (width - len(label)) * " " + label + " "
		while True:
			v = w.inputPwd(s)

			if v is None:
				return False, None

			try:
				v = self.check(v)
				return True, v
			except Exception as ee:
				print("ERROR: " + str(ee))
				continue
	#

	def _doInputPwd1(self, w:_IOutputWriter2, width:int, outReturnValues:dict) -> bool:
		bOkay, v = self.__doInputPwd(w, self.label, width)
		if not bOkay:
			return False

		outReturnValues[self.name] = v
		return True
	#

	def _doInputPwd2(self,w:_IOutputWriter2,  width:int, outReturnValues:dict) -> bool:
		while True:
			bOkay, v1 = self.__doInputPwd(w, self.label, width)
			if not bOkay:
				return False

			bOkay, v2 = self.__doInputPwd(w, self.label2, width)
			if not bOkay:
				return False

			if v1 != v2:
				print("ERROR: Passwords do not match!")
				continue

			outReturnValues[self.name] = v1
			return True
	#

	def _doInputStd(self, w:_IOutputWriter2, width:int, outReturnValues:dict) -> bool:
		bOkay, v = self.__doInputStd(w, self.label, width)
		if not bOkay:
			return False

		outReturnValues[self.name] = v
		return True
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def check(self, argValue):
		if argValue is None:
			if self.paramDef.nullable:
				return
			else:
				raise Exception("Value for form element '" + self.name + "' is null!")
		else:
			if self.typeParser is not None:
				assert isinstance(argValue, str)
				argValue = self.typeParser(argValue)

		argType = type(argValue)

		selectedParamDef = None
		while True:
			if isinstance(self.paramDef.dtype, type):
				if (self.paramDef.dtype == argType) or issubclass(argType, self.paramDef.dtype):
					selectedParamDef = self.paramDef
					break
			# check special types
			elif isinstance(self.paramDef.dtype, str):
				if jk_paramsassert.ParamDefTypeManager.checkSpecialType(self.paramDef.dtype, argValue):
					selectedParamDef = self.paramDef
					break
				if issubclass(argType, object):
					# an object has been specified. perform test by converting all class names to strings.
					# TODO: make this more efficient by not generating all class names fist and then do a match but by doing this at the same time
					typeNames = set()
					typeNames.add(self.__getFullNameFromType(argType))
					for clz in argType.__bases__:
						typeNames.add(self.__getFullNameFromType(clz))
					typeNames.add(argType.__name__)
					for clz in argType.__bases__:
						typeNames.add(clz.__name__)
					if paramDef.argType in typeNames:
						selectedParamDef = paramDef
						break
			else:
				raise Exception("Implementation Error!")

		if selectedParamDef is None:
			raise Exception("Value for form element '" + self.name + "' is of type " + jk_paramsassert.ParamDefTypeManager.typesToStr(argType)
				+ " and not of type " + jk_paramsassert.ParamDefTypeManager.typesToStr([ self.paramDef.dtypes ]) + " as expected!")
		else:
			selectedParamDef.check(argValue)

		return argValue
	#

	def doInput(self, w:_IOutputWriter2, width:int, outReturnValues:dict) -> bool:
		if self.uiAction == "pwd":
			return self._doInputPwd1(w, width, outReturnValues)
		elif self.uiAction == "pwd2":
			return self._doInputPwd2(w, width, outReturnValues)
		else:
			return self._doInputStd(w, width, outReturnValues)
	#

#


















