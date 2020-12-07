



import jk_logging
import jk_prettyprintobj

from thaniya_server.usermgr.BackupUserManager import BackupUserManager






class _UploadStateData(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		self.peerNetworkAddress = None					# str
		self.backupUser = None							# BackupUser
		self.allocationTime = None						# float
		self.completionTime = None						# float
		self.lastUsedByClientTime = None				# float
		self.systemUserPwd = None						# str
		self.localIPAddress = None						# str
		self.estimatedTotalBytesToUpload = None			# int
		self.log = jk_logging.StringListLogger.create()	# jk_logging.StringListLogger
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"peerNetworkAddress",
			"backupUser",
			"allocationTime",
			"completionTime",
			"lastUsedByClientTime",
			"systemUserPwd",
			"localIPAddress",
			"estimatedTotalBytesToUpload",
			"log",
		]
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def toJSON(self) -> dict:
		return {
			"peerNetworkAddress": self.peerNetworkAddress,
			"backupUser": self.backupUser.userName,
			"allocationTime": self.allocationTime,
			"completionTime": self.completionTime,
			"lastUsedByClientTime": self.lastUsedByClientTime,
			"systemUserPwd": self.systemUserPwd,
			"localIPAddress": self.localIPAddress,
			"estimatedTotalBytesToUpload": self.estimatedTotalBytesToUpload,
			"log": self.log.toList(),
		}
	#

	@staticmethod
	def fromJSON(jData:dict, backupUserManager:BackupUserManager):
		ret = _UploadStateData()
		ret.peerNetworkAddress = jData["peerNetworkAddress"]
		ret.backupUser = backupUserManager.getUserE(jData["backupUser"])
		ret.allocationTime = jData["allocationTime"]
		ret.completionTime = jData["completionTime"]
		ret.lastUsedByClientTime = jData["lastUsedByClientTime"]
		ret.systemUserPwd = jData["systemUserPwd"]
		ret.localIPAddress = jData["localIPAddress"]
		ret.estimatedTotalBytesToUpload = jData["estimatedTotalBytesToUpload"]
		ret.log = jk_logging.StringListLogger.create(existingLogLines = jData["log"])
		return ret
	#

#










