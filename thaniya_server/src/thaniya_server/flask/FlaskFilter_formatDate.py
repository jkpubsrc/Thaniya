


import jk_utils

import datetime

from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_formatDate(AbstractFlaskTemplateFilter):

	def __call__(self, value):
		if value is None:
			return ""

		if isinstance(value, (int, float)):
			t = jk_utils.TimeStamp.parse(value)
			return t.dateTime.strftime("%Y-%m-%d")
		elif isinstance(value, jk_utils.TimeStamp):
			return value.dateTime.strftime("%Y-%m-%d")
		elif isinstance(value, datetime.datetime):
			return value.strftime("%Y-%m-%d")
		else:
			return str(value)
	#

#








