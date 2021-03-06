


class APIError(Exception):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, errID:str, errMsg:str = None):
		assert isinstance(errID, str)

		super().__init__(("ERROR: " + errID) if errMsg is None else errMsg)

		self.errID = errID
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#










