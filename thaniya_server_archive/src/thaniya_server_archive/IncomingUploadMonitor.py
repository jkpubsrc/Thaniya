

import re
import os
import typing

import jk_typing
import jk_json
import jk_logging

from thaniya_server.jobs import EnumJobState
from thaniya_server.jobs import Job
from thaniya_server.jobs import JobQueue
from thaniya_server import ServerBackupUploadInfo






class IncomingUploadMonitor(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self, incomingDirPath:str, jobQueue:JobQueue):
		assert os.path.isdir(incomingDirPath)
		assert os.path.isabs(incomingDirPath)

		self.__incomingDirPath = incomingDirPath

		self.__jobQueue = jobQueue
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __markAsScheduled(self, dirPath:str):
		p = os.path.join(dirPath, "_scheduled")
		with open(p, "w") as f:
			pass
	#

	def __isScheduled(self, dirPath:str) -> bool:
		p = os.path.join(dirPath, "_scheduled")
		return os.path.exists(p)
	#

	def __processDir(self, dirPath:str, log:jk_logging.AbstractLogger):
		log.notice("Analyzing incoming: " + os.path.basename(dirPath))

		# load the data provided by the server

		sbui = ServerBackupUploadInfo.loadFromDir(dirPath)

		# load the data provided by the client

		# TODO: use proper file object for this
		jStats = jk_json.loadFromFile(os.path.join(dirPath, "_backup_stats.json"))		# TODO: move this file name to some kind of `constants.py`
		assert jStats["magic"]["magic"] == "thaniya-client-stats"
		jData = jStats["data"]
		assert jData["bSuccess"]

		# collect all files

		dataFileNames = []
		metaFileNames = []

		for fe in os.scandir(dirPath):
			if not fe.is_file():
				pass
			if fe.name[0] == "_":
				metaFileNames.append(fe.name)
			else:
				dataFileNames.append(fe.name)

		# mark as scheduled

		self.__markAsScheduled(dirPath)

		# schedule job

		log.notice("Scheduling job for: " + os.path.basename(dirPath))
		self.__jobQueue.scheduleJob("InsertBackupIntoArchive", 10, {
			"dirPath": dirPath,
			"dataFileNames": dataFileNames,
			"metaFileNames": metaFileNames,
			"tBackupStart": sbui.data["tAllocation"],
			"tBackupEnd": sbui.data["tCompletion"],
			"dClientBackupDuration": sbui.data["tCompletion"] - sbui.data["tAllocation"],
			"sizeInBytes": sbui.data["estimatedTotalBytesToUpload"],
			"systemName": jData["hostName"],
			"backupUserName": sbui.data["backupUser"],
			"backupIdentifier": jData["backupIdentifier"],
		})
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def checkForIncoming(self, log:jk_logging.AbstractLogger):
		for fe in os.scandir(self.__incomingDirPath):
			if not fe.is_dir():
				continue
			if self.__isScheduled(fe.path):
				continue

			with log.descend("Found: " + fe.name) as log2:
				self.__processDir(fe.path, log2)
	#

#













