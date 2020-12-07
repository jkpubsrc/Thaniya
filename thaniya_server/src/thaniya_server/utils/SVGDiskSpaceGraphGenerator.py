

import typing

import jk_typing
from jk_svg import *

from jk_appmonitoring import RDiskSpacePart
from jk_appmonitoring import RFileSystem




_CSS_COLOR_OTHER = "#406040"
_CSS_COLOR_RESERVED = "#604040"
_CSS_COLOR_FREE = "#40ff00"
_CSS_COLORS_USED = (
	"#00ffe0",
	"#00c0ff",
	"#0080ff",
	"#006080",
)




class _SVGBarPart(RDiskSpacePart):

	def __init__(self, part:RDiskSpacePart, cssColor:str, bSmall:bool):
		super().__init__(
			part.name,
			part.dirPath,
			part.diskSpaceUsed,
			part.fsSizeTotal,
			part.partType,
		)
		self.cssColor = cssColor
		self.bSmall = bSmall
	#

#





class SVGDiskSpaceGraphGenerator(object):

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

		self.__usages = []				# _SVGBarPart[]

		availableColors = list(_CSS_COLORS_USED)
		for u in filesystem.usages:
			if u.partType == "free":
				col = _CSS_COLOR_FREE
				bSmall = True
			elif u.partType == "reserved":
				col = _CSS_COLOR_RESERVED
				bSmall = True
			elif u.partType == "usedOther":
				col = _CSS_COLOR_OTHER
				bSmall = True
			else:
				if not availableColors:
					raise Exception("Too many sections!")
				col = availableColors[0]
				del availableColors[0]
				bSmall = False
			self.__usages.append(_SVGBarPart(u, col, bSmall))

		# ----

		self.textCSSColor = "#ffffff"
		self.textFontFamily = "Arial"
		self.boxFrameCSSColor = None
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

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def toSVG(self, width:int) -> str:
		assert width > 0

		# ----

		svg = SVGGraphic()

		y = 0
		with svg.createGroup() as g:

			if self.__bGenerateWithTitle:
				with g.createText() as text:
					text.x = 0
					text.y = y + 12
					text.textContent = "{:s} | Total disk space: {:.1f}G ({:.1f}% used)".format(
						self.__name,
						self.__fsSizeTotal / (1024*1024*1024),
						self.__fsSizeUsedPercent,
					)
					text.style = "font-size:16px;"
				y += 25

			x = 0
			for u in self.__usages:

				with g.createRect() as rect:
					w = width * u.diskSpaceUsedFraction
					rect.setBounds(x, y, w, 20)
					rect.style = "fill:" + u.cssColor
					x += w

			if self.boxFrameCSSColor:
				with g.createRect() as rect:
					rect.setBounds(0, y, width, 20)
					rect.style = "fill:none;stroke:{};stroke-width:1px".format(boxFrameCSSColor)

		y += 25
		ymax = y
		yTextHeight = 20

		with svg.createGroup() as g:

			x = 0
			for u in self.__usages:

				with g.createCircle() as circle:
					circle.setCenter(x + 10, y + 15)
					if u.bSmall:
						circle.r = 6
					else:
						circle.r = 10
					circle.style = "fill:" + u.cssColor

				if not u.bSmall:
					with g.createCircle() as circle:
						circle.setCenter(x + 10, y + 15)
						circle.r = 3
						circle.style = "fill:#000"		# TODO: this is a colored circle with a second black middle circle; make the middle circle transparent => this here should be a ring!

				with g.createText() as text:
					text.x = x + 30
					text.y = y + 20
					text.textContent = "{:s}: {:.1f}G ({:.1f}%)".format(
						u.name,
						u.diskSpaceUsed / (1024*1024*1024),
						u.diskSpaceUsedFraction * 100,
					)
					ymax = y + yTextHeight
					
				x += 280
				if x > width - 280:
					x = 0
					y += yTextHeight

		svg.cssStyleLines = [
			"text {",
			"\tfill:{};".format(self.textCSSColor) if self.textCSSColor else "",
			"\tfont-family:{};".format(self.textFontFamily) if self.textFontFamily else "",
			"\tfont-size:12px;",
			"\tstroke:none;",
			"}"
		]

		svg.attributes["viewBox"] = "0 0 {}px {}px".format(width, ymax)
		svg.attributes["width"] = "{}px".format(width)
		svg.attributes["height"] = "{}px".format(ymax)

		return svg.toSVG(bPretty=True, bWithXMLDeclaration=self.__bGenerateWithXMLDeclaration)
	#











#




