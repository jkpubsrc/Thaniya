



from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_boolToYesNo(AbstractFlaskTemplateFilter):

	def __call__(self, value:bool):
		if value is None:
			return ""
		if value:
			return "yes"
		else:
			return "no"
	#

#








