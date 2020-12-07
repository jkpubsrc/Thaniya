



import jk_utils

from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_formatPercent(AbstractFlaskTemplateFilter):

	def __call__(self, value:float):
		if value is None:
			return ""
		return str(round(value * 100, 1)) + "%"
	#

#








