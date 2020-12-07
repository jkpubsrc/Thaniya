



from .AbstractFlaskTemplateFilter import AbstractFlaskTemplateFilter





#
# Generates an identifier that only contains "a-zA-Z0-9" from an arbitrary string.
#
class FlaskFilter_strToID(AbstractFlaskTemplateFilter):

	def __call__(self, text):
		if text is None:
			return ""

		ret = []
		for c in text:
			if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
				ret.append(c)
			else:
				ret.append(str(ord(c)))
		return "".join(ret)
	#

#








