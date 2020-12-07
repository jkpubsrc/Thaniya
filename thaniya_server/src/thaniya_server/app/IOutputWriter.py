# NOTE: This is a copy from ~/DevPriv/PythonProjects/MediaWikiMgmt/jk_mediawikirepo/src/jk_mediawikirepo/app/*



import jk_console
import jk_pwdinput

from ._IOutputWriter2 import _IOutputWriter2
from .CLIForm import CLIForm






class IOutputWriter(_IOutputWriter2):

	def _dataToStr(self, *args):
		raise NotImplementedError()
	#

	def printTable(self, table:jk_console.SimpleTable):
		for line in table.printToLines():
			self._print(self._dataToStr(line))
	#

	def print(self, *args):
		self._print(self._dataToStr(*args))
	#

	def inputStd(self, *args):
		return input(self._dataToStr(*args))
	#

	def inputPwd(self, *args):
		return jk_pwdinput.readpwd(self._dataToStr(*args))
	#

	def createForm(self) -> CLIForm:
		return CLIForm(self)
	#

#





