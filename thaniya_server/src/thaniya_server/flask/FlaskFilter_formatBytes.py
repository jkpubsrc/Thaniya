



import jk_utils

from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_formatBytes(AbstractFlaskTemplateFilter):

	def __call__(self, value:float):
		if value is None:
			return ""
		return jk_utils.formatBytes(float(value))
	#

#








