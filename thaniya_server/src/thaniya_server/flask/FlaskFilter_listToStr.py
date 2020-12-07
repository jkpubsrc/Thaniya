



from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# Creates a canonical string represetation of data.
#
class FlaskFilter_listToStr(AbstractFlaskTemplateFilter):

	def __call__(self, value:list):
		return ", ".join(value)
	#

#








