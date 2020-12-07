

import os
import shutil

import jk_utils
import jk_argparsing
import jk_mounting
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from .AppRuntimeServerCtrl import AppRuntimeServerCtrl

from .TextDiskSpaceGraphGenerator import TextDiskSpaceGraphGenerator

from thaniya_server_archive.volumes import Device
from thaniya_server_archive.volumes import BackupVolumeID
from thaniya_server_archive.volumes import BackupVolumeInfo
from thaniya_server_archive.volumes import BackupVolumeManager







class _CLICmd_volume_create_directory(CLICmdBase):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, appRuntime:AppRuntimeServerCtrl):
		self.__appRuntime = appRuntime
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def cmdName(self) -> str:
		return "vol-create-static"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "Register a directory statically as backup volumes."
	#

	@property
	def usesOutputWriter(self) -> bool:
		return True
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def registerCmd(self, ap:jk_argparsing.ArgsParser) -> jk_argparsing.ArgCommand:
		argCmd = super().registerCmd(ap)
		argCmd.expectString("dir", minLength=1)
	#

	def _runImpl(self, p:CLICmdParams) -> bool:
		with p.out.section("Register directory as backup volume") as out:

			dirPath = p.cmdArgs[0]
			if not os.path.isdir(dirPath):
				raise Exception("Not a directory: " + dirPath)

			with p.log.descend("Now creating new backup volume using: " + dirPath) as log2:
				backupVolumeID = self.__appRuntime.backupVolumeMgr.createDirectoryVolume(dirPath, log2)
				#out.print("Backup volume has been created: " + backupVolumeID.hexData)

			self.__appRuntime.updateFileSystemCollection()
			self.__appRuntime.notifyOtherThaniyaProcesses()
	#

#





