

import typing

import jk_typing
import jk_console

from jk_appmonitoring import RDiskSpacePart
from jk_appmonitoring import RFileSystem




_TEXT_COLOR_OTHER = jk_console.Console.ForeGround.STD_DARKGRAY
_TEXT_COLOR_RESERVED = jk_console.Console.ForeGround.STD_PURPLE
_TEXT_COLOR_FREE = jk_console.Console.ForeGround.STD_LIGHTGREEN
_TEXT_COLORS_USED = (
	jk_console.Console.ForeGround.STD_LIGHTCYAN,
	jk_console.Console.ForeGround.STD_CYAN,
	jk_console.Console.ForeGround.STD_BLUE,
	jk_console.Console.ForeGround.STD_LIGHTBLUE,
)




class _TextBarPart(RDiskSpacePart):

	def __init__(self, part:RDiskSpacePart, textColor:str, character:str, bSmall:bool):
		super().__init__(
			part.name,
			part.dirPath,
			part.diskSpaceUsed,
			part.fsSizeTotal,
			part.partType,
		)
		self.textColor = textColor
		self.character = character
		self.bSmall = bSmall
	#

#





class TextDiskSpaceGraphGenerator(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, filesystem:RFileSystem, bGenerateWithTitle:bool = False, bGenerateWithXMLDeclaration:bool = False):
		self.__bGenerateWithTitle = bGenerateWithTitle
		self.__bGenerateWithXMLDeclaration = bGenerateWithXMLDeclaration

		self.__name = filesystem.name
		self.__mountPoint = filesystem.mountPoint
		self.__devicePath = filesystem.devicePath

		# ----

		self.__fsSizeTotal = filesystem.fsSizeTotal
		self.__fsSizeUsedPercent = filesystem.fsSizeUsedPercent

		# ----

		self.__usages = []				# _TextBarPart[]

		availableColors = list(_TEXT_COLORS_USED)
		for u in filesystem.usages:
			if u.partType == "free":
				c = "█"
				col = _TEXT_COLOR_FREE
				bSmall = True
			elif u.partType == "reserved":
				#c = "▒"
				c = "█"
				col = _TEXT_COLOR_RESERVED
				bSmall = True
			elif u.partType == "usedOther":
				#c = "▒"
				c = "█"
				col = _TEXT_COLOR_OTHER
				bSmall = True
			else:
				if not availableColors:
					raise Exception("Too many sections!")
				c = "█"
				col = availableColors[0]
				del availableColors[0]
				bSmall = False
			self.__usages.append(_TextBarPart(u, col, c, bSmall))

	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def mountPoint(self) -> str:
		return self.__mountPoint
	#

	@property
	def name(self) -> str:
		return self.__name
	#

	@property
	def devicePath(self) -> str:
		return self.__devicePath
	#

	@property
	def title(self) -> str:
		return "{:s}&nbsp;&nbsp;|&nbsp;&nbsp;Total&nbsp;disk&nbsp;space:&nbsp;{:.1f}G&nbsp;({:.1f}%&nbsp;used)".format(
			self.__name,
			self.__fsSizeTotal / (1024*1024*1024),
			self.__fsSizeUsedPercent,
		)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __rect(self, width:int, color:str, character:str) -> str:
		return color + character * width + jk_console.Console.RESET
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def toStr(self) -> str:
		width = jk_console.Console.width() - 3 - 2
		ret = []

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# >>>> add header

		ret.append(
			(
				"  "
				+ jk_console.Console.BOLD
				+ jk_console.Console.ForeGround.STD_LIGHTCYAN
				+ "{:s} | Total disk space: {:.1f}G ({:.1f}% used)"
				+ jk_console.Console.RESET
			).format(
				self.__name,
				self.__fsSizeTotal / (1024*1024*1024),
				self.__fsSizeUsedPercent,
			)
		)

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		ret.append("")

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# >>>> calculate the bars

		# first calculate all widths
		barSizes = []
		for u in self.__usages:
			w = int(round(width * u.diskSpaceUsedFraction))
			barSizes.append(w)

		# identify the largest bar
		iLargest = 0
		iLargestW = barSizes[0]
		for i in range(1, len(barSizes)):
			if barSizes[i] > iLargestW:
				iLargestW = barSizes[i]
				iLargest = i

		# if a section is invisible: take space from largest bar
		for i in range(0, len(barSizes)):
			if barSizes[i] == 0:
				barSizes[i] = 1
				barSizes[iLargest] -= 1

		# now generate the color bars
		_temp = [ "  " ]
		for u, barSize in zip(self.__usages, barSizes):
			_temp.append(self.__rect(barSize, u.textColor, u.character))
		ret.append("".join(_temp))

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		ret.append("")

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# >>>> add legend

		_temp = ""
		for u in self.__usages:
			_temp2 = u.textColor + ("●" if u.bSmall else "🞉") + jk_console.Console.RESET + " "
			_temp2 += "{:s}: {:.1f}G ({:.1f}%)".format(
				u.name,
				u.diskSpaceUsed / (1024*1024*1024),
				u.diskSpaceUsedFraction * 100,
			)
			if _temp and (len(_temp) + 2 + len(_temp2) >= width):
				ret.append(_temp)
				_temp = ""
			_temp += "  " + _temp2

		if _temp:
			ret.append(_temp)

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		return "\n".join(ret)
	#











#




