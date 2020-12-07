



from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# Creates a canonical string represetation of data.
#
class FlaskFilter_toStr(AbstractFlaskTemplateFilter):

	def __call__(self, data):
		if data is None:
			return ""
		elif data is True:
			return "true"
		elif data is False:
			return "false"
		return str(data)
	#

#








