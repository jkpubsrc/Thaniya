# NOTE: This is a copy from ~/DevPriv/PythonProjects/MediaWikiMgmt/jk_mediawikirepo/src/jk_mediawikirepo/app/*



import jk_console

from .CLIForm import CLIForm
from .IOutputWriter import IOutputWriter

FG = jk_console.Console.ForeGround

SECTION_COLOR = FG.STD_LIGHTCYAN
SUBSECTION_COLOR = FG.STD_LIGHTCYAN








class _PrintSubSection(IOutputWriter):

	def __init__(self, printer, prefix:str, title:str, bColor:bool = True, color:str = None):
		assert printer
		assert isinstance(prefix, str)
		assert isinstance(title, str)
		assert isinstance(bColor, bool)
		if color is None:
			if bColor:
				color = SECTION_COLOR
		if color is None:
			color = ""
			colorReset = ""
		else:
			assert isinstance(color, str)
			colorReset = jk_console.Console.RESET

		self.__color = color
		self.__bColor = bColor
		self.__printer = printer
		self._print = printer.print
		self._print(color + prefix + title + colorReset)
		self.__prefix = prefix
	#

	def __enter__(self):
		return self
	#

	def _dataToStr(self, *args):
		return self.__prefix + "⸽  " + " ".join([ str(a) for a in args ])
	#

	def __exit__(self, exClazz, exObj, exStackTrace):
		self._print(self.__prefix + "⸌┈")
		self._print()
	#

#

class _PrintSection(IOutputWriter):

	def __init__(self, printer, title:str, bColor:bool = True, color:str = None):
		assert printer
		assert isinstance(title, str)
		if color is None:
			if bColor:
				color = SECTION_COLOR
		if color is None:
			color = ""
			colorReset = ""
		else:
			assert isinstance(color, str)
			colorReset = jk_console.Console.RESET

		self.__color = color
		self.__bColor = bColor
		self.__printer = printer
		self._print = printer.print
		self._print()
		self._print(color + ">"*120 + colorReset)
		self._print(color + ">>>>>>>>  " + title + "  " + colorReset)
		self._print(color + ">"*120 + colorReset)
		self._print()
	#

	def __enter__(self):
		return self
	#

	def subsection(self, *args, color:str = None) -> _PrintSubSection:
		assert len(args) > 0
		title = " ".join([str(a) for a in args])
		if color is None:
			color = self.__color
		return _PrintSubSection(self.__printer, "  ", title, self.__bColor, color)
	#

	def _dataToStr(self, *args):
		return "  " + " ".join([ str(a) for a in args ])
	#

	def __exit__(self, exClazz, exObj, exStackTrace):
		self._print()
	#

#

class OutputWriter(IOutputWriter):

	################################################################################################################################
	## Constructor Methods
	################################################################################################################################

	def __init__(self, bColor:bool = True):
		self.__bLastLineWasEmpty = False
		self.__bHadOutput = False
		self._print = self.print
		self.__bColor = bColor
		self.__buffer = []
		self.__bAutoFlush = False
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def autoFlush(self) -> bool:
		return self.__bAutoFlush
	#

	@autoFlush.setter
	def autoFlush(self, value:bool):
		assert isinstance(value, bool)
		self.__bAutoFlush = value
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __printToBuffer(self, *args):
		s = " ".join([ str(a) for a in args ])
		self.__buffer.append(s)

		if self.__bAutoFlush:
			self.flush()
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def print(self, *args):
		text = " ".join([ str(a) for a in args ])
		text = text.rstrip()
		if len(text) == 0:
			if not self.__bLastLineWasEmpty:
				self.__buffer.append("")
				self.__bLastLineWasEmpty = True
		else:
			self.__buffer.append(text)
			self.__bLastLineWasEmpty = False
			self.__bHadOutput = True

		if self.__bAutoFlush:
			self.flush()
	#

	def _dataToStr(self, *args):
		return " ".join([ str(a) for a in args ])
	#

	def section(self, *args, color:str = None) -> _PrintSection:
		assert len(args) > 0
		title = " ".join([str(a) for a in args])
		return _PrintSection(self, title, self.__bColor, color)
	#

	def __enter__(self):
		self.print()
		return self
	#

	def __exit__(self, exClazz, exObj, exStackTrace):
		self.print()
		self.flush()
	#

	def flush(self):
		for line in self.__buffer:
			print(line)
		self.__buffer.clear()
	#

#





