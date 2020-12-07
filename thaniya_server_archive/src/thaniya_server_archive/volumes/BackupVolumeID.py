

import os

from thaniya_server.utils.ID import ID








BACKUP_VOLUME_ID_LENGTH = 8



class BackupVolumeID(ID):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, idData):
		super().__init__(BACKUP_VOLUME_ID_LENGTH, idData)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@staticmethod
	def generate():
		while True:
			dsi = BackupVolumeID(os.urandom(BACKUP_VOLUME_ID_LENGTH))
			if dsi.isNotEmpty():
				return dsi
	#

	@staticmethod
	def parseFromStr(text):
		assert isinstance(text, str)
		#binData = BackupVolumeID._parseBinaryFromString(BackupVolumeID.__name__, text)
		binData = BackupVolumeID._tryParseBinaryFromString(BackupVolumeID.__name__, text)
		if binData is None:
			binData = BackupVolumeID._tryParseHexFromString(text)
		if binData is None:
			raise Exception("Failed to parse: " + text)
		return BackupVolumeID(binData)
	#

	@staticmethod
	def parseFromHexStr(text):
		assert isinstance(text, str)
		binData = BackupVolumeID._tryParseHexFromString(text)
		if binData is None:
			raise Exception("Failed to parse: " + text)
		return BackupVolumeID(binData)
	#

	@staticmethod
	def fromBinary(byteData):
		return BackupVolumeID(byteData)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

#



BackupVolumeID.EMPTY = BackupVolumeID(bytearray(BACKUP_VOLUME_ID_LENGTH))











