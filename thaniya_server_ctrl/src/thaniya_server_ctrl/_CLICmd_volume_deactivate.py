

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







class _CLICmd_volume_deactivate(CLICmdBase):

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
		return "vol-deactivate"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "Deactivate a backup volume."
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
		argCmd.expectString("id", minLength=1)
	#

	def _runImpl(self, p:CLICmdParams) -> bool:
		with p.out.section("Deactivate backup volume") as out:

			volumeID = BackupVolumeID.parseFromStr(p.cmdArgs[0])
			with p.log.descend("Now deactivating: " + str(volumeID.hexData)) as log2:
				self.__appRuntime.backupVolumeMgr.deactivateVolume(volumeID, log2)
	#

#





