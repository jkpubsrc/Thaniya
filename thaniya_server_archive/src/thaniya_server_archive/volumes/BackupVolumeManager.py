

import typing
import re
import os

import jk_typing
import jk_json
import jk_utils
import jk_logging
import jk_prettyprintobj

from .BackupVolumeID import BackupVolumeID
from .BackupVolumeCfgFile import BackupVolumeCfgFile
from .DeviceIterator import DeviceIterator
from .Device import Device
from .BackupVolumeInfo import BackupVolumeInfo





def _ensureDirExists(dirPath:str, bCreateMissingDirectories:bool):
	if not os.path.isdir(dirPath):
		if bCreateMissingDirectories:
			os.makedirs(dirPath, exist_ok=True)
		else:
			raise Exception("No such directory: " + dirPath)
	os.chmod(dirPath, jk_utils.ChModValue("rwx------").toInt())
#




#
# This class manages all backup volumes.
#
class BackupVolumeManager(object):

	################################################################################################################################
	## Constructor Method
	################################################################################################################################

	#
	# @param		str varDirPath			The main <c>var</c> directory that is used to store variable data. This should be something like
	#										"/var/thaniya/httpd" or "/srv/thaniya/httpd". It must be readable and writable as this object
	#										here will make changes to subdirectories.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, staticVolumeCfgDirPath:str, stateDirPath:str, log:jk_logging.AbstractLogger, bCreateMissingDirectories:bool = True):
		# stores information which volumes are active; this is part of the runtime information;
		self.__thaniyaStateDirPath = stateDirPath
		_ensureDirExists(self.__thaniyaStateDirPath, bCreateMissingDirectories)
		self.__thaniyaStateFilePath = os.path.join(self.__thaniyaStateDirPath, "BackupVolumeManager.json")

		# stores registration records about volumes; this is part of the configuration;
		self.__thaniyaStaticVolumeCfgDirPath = staticVolumeCfgDirPath
		_ensureDirExists(self.__thaniyaStaticVolumeCfgDirPath, bCreateMissingDirectories)

		# ----

		self.__activeVolumes = set()					# this set stores BackupVolumeID objects; every volume registered here is considered as being active;

		self.__loadState(log)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __loadState(self, log:jk_logging.AbstractLogger):
		activeVolumes = set()
		if os.path.isfile(self.__thaniyaStateFilePath):
			if log:
				log.notice("Loading state from: " + self.__thaniyaStateFilePath)
			jData = jk_json.loadFromFile(self.__thaniyaStateFilePath)
			assert jData["magic"]["magic"] == "thaniya-state-BackupVolumeManager"
			assert jData["magic"]["version"] == 1
			for x in jData["activeVolumes"]:
				try:
					activeVolumes.add(BackupVolumeID.parseFromStr(x))
				except Exception as ee:
					log.error(ee)
		self.__activeVolumes = activeVolumes
	#

	def __storeState(self, log:jk_logging.AbstractLogger = None):
		jActiveVolumes = []
		for va in self.__activeVolumes:
			jActiveVolumes.append(str(va))

		jData = {
			"magic": {
				"magic": "thaniya-state-BackupVolumeManager",
				"version": 1,
			},
			"activeVolumes": jActiveVolumes
		}

		if log:
			log.notice("Persisting state to: " + self.__thaniyaStateFilePath)

		with jk_utils.file_rw.openWriteJSON(self.__thaniyaStateFilePath, bSafeWrite=True, bPretty=True) as f:
			f.write(jData)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def update(self, log:jk_logging.AbstractLogger):
		self.__activeVolumes = set()					# this set stores BackupVolumeID objects; every volume registered here is considered as being active;
		self.__loadState(log)
	#

	@jk_typing.checkFunctionSignature()
	def isActive(self, backupVolumeID:typing.Union[BackupVolumeID,str]):
		if isinstance(backupVolumeID, str):
			backupVolumeID = BackupVolumeID.parseFromStr(backupVolumeID)

		return backupVolumeID in self.__activeVolumes
	#

	def deactivateVolume(self, backupVolumeID:typing.Union[BackupVolumeID,str], log:jk_logging.AbstractLogger = None):
		if isinstance(backupVolumeID, str):
			backupVolumeID = BackupVolumeID.parseFromStr(backupVolumeID)

		v = self.getVolumeE(backupVolumeID, log)
		if not v.isActive:
			raise Exception("Backup volume " + str(backupVolumeID) + " is not active!")

		self.__activeVolumes.remove(backupVolumeID)

		self.__storeState(log)
	#

	def activateVolume(self, backupVolumeID:typing.Union[BackupVolumeID,str], log:jk_logging.AbstractLogger = None):
		if isinstance(backupVolumeID, str):
			backupVolumeID = BackupVolumeID.parseFromStr(backupVolumeID)

		v = self.getVolumeE(backupVolumeID, log)
		if v.isActive:
			raise Exception("Backup volume " + str(backupVolumeID) + " is already active!")

		self.__activeVolumes.add(backupVolumeID)

		self.__storeState(log)
	#

	@jk_typing.checkFunctionSignature()
	def getVolume(self, backupVolumeID:typing.Union[BackupVolumeID,str], log:jk_logging.AbstractLogger) -> typing.Union[BackupVolumeInfo]:
		if isinstance(backupVolumeID, str):
			backupVolumeID = BackupVolumeID.parseFromStr(backupVolumeID)

		for v in self.listVolumes(log):
			if v.backupVolumeID == backupVolumeID:
				return v
		return None
	#

	@jk_typing.checkFunctionSignature()
	def getVolumeE(self, backupVolumeID:typing.Union[BackupVolumeID,str], log:jk_logging.AbstractLogger) -> typing.Union[BackupVolumeInfo]:
		if isinstance(backupVolumeID, str):
			backupVolumeID = BackupVolumeID.parseFromStr(backupVolumeID)

		for v in self.listVolumes(log):
			if v.backupVolumeID == backupVolumeID:
				return v
		raise Exception("No such backup volume: " + str(backupVolumeID))
	#

	@jk_typing.checkFunctionSignature()
	def listVolumes(self, log:jk_logging.AbstractLogger) -> typing.List[BackupVolumeInfo]:
		ret = []

		with log.descend("Listing backup volumes ...") as log2:
			log2.notice("Scanning directory: " + self.__thaniyaStaticVolumeCfgDirPath)
			for fe in os.scandir(self.__thaniyaStaticVolumeCfgDirPath):
				if fe.is_file():
					if re.match("^volume-info-[a-zA-Z0-9]+.json$", fe.name):
						log2.notice("Loading: " + fe.path)
						try:
							f = BackupVolumeCfgFile.loadFromFile(fe.path)
							mountPoint = jk_utils.fsutils.findMountPoint(f.getValue("backupBaseDirPath"))
							device = DeviceIterator.getMountedDevice(mountPoint)
							ret.append(
								BackupVolumeInfo(self, "configured-directory", device, f.getValue("volumeID"), f.getValue("backupBaseDirPath"), fe.path)
							)
						except Exception as ee:
							log2.error(ee)

		return ret
	#

	#
	# Create a volume based on an always existing, standard directory in the system.
	#
	# These type of backup volumes are ment for systems where disks are mounted on boot and remain in the systems forever. In that case you simply might
	# configure a volume instead on relying on autodetect. Moreover this kind of configuration is well suited for testing.
	#
	@jk_typing.checkFunctionSignature()
	def createDirectoryVolume(self, backupBaseDirPath:str, log:jk_logging.AbstractLogger = None) -> BackupVolumeID:
		backupBaseDirPath = os.path.normpath(backupBaseDirPath)

		with log.descend("Creating new volume for: " + backupBaseDirPath) as log2:

			# check target

			if not os.path.isdir(backupBaseDirPath):
				raise Exception("Not a directory: " + backupBaseDirPath)
			if not os.path.isabs(backupBaseDirPath):
				raise Exception("Directory must be an absolute path: " + backupBaseDirPath)

			bIsEmpty = True
			for n in os.listdir(backupBaseDirPath):
				bIsEmpty = False
				break
			if not bIsEmpty:
				raise Exception("Directory is not empty: " + backupBaseDirPath)

			# we need to know all existing volumes -> retrieve this data now

			existingVols = self.listVolumes(log2)				# BackupVolumeInfo[]

			# check target: this might already be configured

			if os.path.isfile(os.path.join(backupBaseDirPath, "THANIYA_INFO", "volume-info.json")):
				raise Exception("Device seems to be a Thaniya backup volume: " + backupBaseDirPath)

			if os.path.isdir(os.path.join(backupBaseDirPath, "THANIYA_DATA")):
				raise Exception("Device seems to be a Thaniya backup volume: " + backupBaseDirPath)

			knownBackupIDs = set()
			for v in existingVols:
				knownBackupIDs.add(v.backupVolumeID)
				if v.backupBaseDirPath == backupBaseDirPath:
					raise Exception("Directory path is already in use for a backup volume: " + backupBaseDirPath)
				if backupBaseDirPath.startswith(v.backupBaseDirPath):
					raise Exception("Directory path is a subdirectory of another backup volume: " + backupBaseDirPath)

			# find a new backup volume ID

			while True:
				backupVolumeID = BackupVolumeID.generate()
				if backupVolumeID in knownBackupIDs:
					continue
				thaniyaVolumeInfoFilePath = os.path.join(self.__thaniyaStaticVolumeCfgDirPath, "volume-info-" + backupVolumeID.hexData + ".json")
				if os.path.isfile(thaniyaVolumeInfoFilePath):
					continue
				break

			# create backup volume data structure

			volumeInfoFile = BackupVolumeCfgFile()
			volumeInfoFile.setValue("volumeID", backupVolumeID)
			volumeInfoFile.setValue("backupBaseDirPath", backupBaseDirPath)
			volumeInfoFile.setValue("isActive", True)

			# persist the configuration data

			log2.notice("Creating file: " + thaniyaVolumeInfoFilePath)
			volumeInfoFile.writeToFile(thaniyaVolumeInfoFilePath)

			# ----

			return backupVolumeID
	#

#






















