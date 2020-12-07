


from flask import Markup

from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# ...
#
class FlaskFilter_tagsColoredToStr(AbstractFlaskTemplateFilter):

	def __call__(self, tags:list):
		if tags:
			temp = []
			for tag in tags:
				temp.append("<span class=\"repoTag\">" + tag + "</span>")
			return Markup(", ".join(temp))
		else:
			return ""
	#

#








