

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







class _CLICmd_volume_activate(CLICmdBase):

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
		return "vol-activate"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "Activate a backup volume."
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
		with p.out.section("Activate backup volume") as out:

			volumeID = BackupVolumeID.parseFromStr(p.cmdArgs[0])
			p.log.notice("Activating: " + str(volumeID.hexData))
			with p.log.descend("Now activating: " + str(volumeID.hexData)) as log2:
				self.__appRuntime.backupVolumeMgr.activateVolume(volumeID, log2)
	#

#





