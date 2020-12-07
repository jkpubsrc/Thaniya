



import json
import base64

from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_j(AbstractFlaskTemplateFilter):

	def __call__(self, jData):
		if jData is None:
			return ""

		s = json.dumps(jData)
		s = base64.b64encode(
			s.encode("utf-8")
		).decode("ascii")
		return s
	#

#








