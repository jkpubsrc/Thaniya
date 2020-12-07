


import jk_utils

import datetime

from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_formatTime(AbstractFlaskTemplateFilter):

	def __call__(self, value):
		if value is None:
			return ""

		if isinstance(value, (int, float)):
			t = jk_utils.TimeStamp.parse(value)
			return t.dateTime.strftime("%H:%M:%S")
		elif isinstance(value, jk_utils.TimeStamp):
			return value.dateTime.strftime("%H:%M:%S")
		elif isinstance(value, datetime.datetime):
			return value.strftime("%H:%M:%S")
		else:
			return str(value)
	#

#








