



from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_tagsToStr(AbstractFlaskTemplateFilter):

	def __call__(self, tags:list):
		if tags:
			return ", ".join(tags)
		else:
			return ""
	#

#








