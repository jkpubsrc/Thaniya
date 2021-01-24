


import jk_utils

import datetime

from babel.dates import format_date, format_datetime, format_time

from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_formatDateHR(AbstractFlaskTemplateFilter):

	def __call__(self, value, locale:str = None):
		if value is None:
			return ""

		print("> FlaskFilter_formatDateHR ::", repr(locale), bool(locale))

		if isinstance(value, str):
			t = datetime.datetime.strptime(value, "%Y-%m-%d")
			if locale:
				return format_date(t, format="long", locale=locale)
			else:
				return t.dateTime.strftime("%Y-%m-%d")
		elif isinstance(value, (int, float)):
			t = jk_utils.TimeStamp.parse(value)
			if locale:
				return format_date(t.dateTime, format="long", locale=locale)
			else:
				return t.dateTime.strftime("%Y-%m-%d")
		elif isinstance(value, jk_utils.TimeStamp):
			if locale:
				return format_date(value.dateTime, format="long", locale=locale)
			else:
				return value.dateTime.strftime("%Y-%m-%d")
		elif isinstance(value, datetime.datetime):
			if locale:
				return format_date(value, format="long", locale=locale)
			else:
				return value.strftime("%Y-%m-%d")
		else:
			return str(value)
	#

#








