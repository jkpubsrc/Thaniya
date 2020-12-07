



import os





class IDCreator(object):

	ID_LENGTH = 64
	ID_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_"

	@staticmethod
	def createID() -> str:
		assert len(IDCreator.ID_CHARACTERS) == IDCreator.ID_LENGTH

		rawRndData = os.urandom(IDCreator.ID_LENGTH)
		ret = "".join([ IDCreator.ID_CHARACTERS[v % IDCreator.ID_LENGTH] for v in rawRndData ])
		return ret
	#

#







