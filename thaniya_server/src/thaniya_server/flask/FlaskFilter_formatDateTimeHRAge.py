


import jk_utils

import datetime

from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_formatDateTimeHRAge(AbstractFlaskTemplateFilter):

	def __call__(self, value):
		if value is None:
			return ""

		if isinstance(value, (int, float, datetime.datetime)):
			t = jk_utils.TimeStamp(value)
			dt = datetime.datetime.utcnow()
			rs = (dt - t.dateTime).total_seconds()
			return jk_utils.duration.secondsToHRStr(rs)
		else:
			return str(value)
	#

#








