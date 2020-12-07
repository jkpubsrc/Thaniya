


import re

import jk_prettyprintobj




class AbstractFlaskTemplateFilter(jk_prettyprintobj.DumpMixin):

	def __init__(self):
		pass
	#

	################################################################################################################################
	#### Helper Methods
	################################################################################################################################

	def _dumpVarNames(self):
		return [
			"name",
		]
	#

	################################################################################################################################
	#### Public Properties
	################################################################################################################################

	@property
	def name(self) -> str:
		s = self.__class__.__name__
		pos = s.find("_")
		if pos <= 0:
			raise Exception("Overwrite this property to return a name or use the underscore naming schema!")
		s = s[pos+1:]
		if not re.match("^[a-zA-Z][a-zA-Z0-9_]*$", s):
			raise Exception("Invalid class name!")
		return s
	#

	################################################################################################################################
	#### Public Methods
	################################################################################################################################

	def __call__(self):
		raise NotImplementedError()
	#

#





