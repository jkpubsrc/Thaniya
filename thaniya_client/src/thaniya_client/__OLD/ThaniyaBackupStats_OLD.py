


import json

import jk_json




#
# Represents status and statistical information about a backup performed.
#
class ThaniyaBackupStats_OLD(object):

	__MAGIC = "thaniya-stats"

	__VALID_KEYS = [
		"magic",
		"version",
		"tStart",
		"tEnd",
		"success",
		"expectedBytesToWrite",
		"totalBytesWritten",
		"avgWritingSpeed",
		"simulate",
		"backupIdentifier",
		"d0_calcDiskSpace",
		"d1_connectAndPrepare",
		"d2_backup",
	]

	def __init__(self):
		self.magic = ThaniyaBackupStats.__MAGIC	# str
		self.version = 1						# int
		self.tStart = None						# float
		self.tEnd = None						# float
		self.success = None						# bool
		self.expectedBytesToWrite = None		# int
		self.totalBytesWritten = None			# int
		self.avgWritingSpeed = None				# float
		self.simulate = None					# bool
		self.backupIdentifier = None			# str
		self.d0_calcDiskSpace = None			# float
		self.d1_connectAndPrepare = None		# float
		self.d2_backup = None					# float
	#

	def writeToFile(self, filePath:str):
		assert isinstance(filePath, str)

		jk_json.saveToFilePretty(self.toJSON(), filePath)
	#

	def toJSON(self) -> dict:
		ret = {}
		for key in ThaniyaBackupStats.__VALID_KEYS:
			ret[key] = getattr(self, key)
		return ret
	#

	def __str__(self):
		return json.dumps(self.toJSON(), indent="\t", sort_keys=True)
	#

	@staticmethod
	def loadFromFile(filePath:str):
		assert isinstance(filePath, str)

		jData = jk_json.loadFromFile(filePath)
		return ThaniyaBackupStats.loadFromJSON(jData)
	#

	@staticmethod
	def loadFromJSON(jData:dict):
		assert isinstance(jData, dict)
		assert jData.get("magic") == ThaniyaBackupStats.__MAGIC
		assert jData.get("version") == 1

		ret = ThaniyaBackupStats()
		for key in ThaniyaBackupStats.__VALID_KEYS:
			setattr(ret, key, jData.get(key))
		return ret
	#

	def setValue(self, name, value):
		if name in ThaniyaBackupStats.__VALID_KEYS:
			setattr(self, name, value)
		else:
			raise Exception("Invalid property name: " + repr(name))
	#

#









