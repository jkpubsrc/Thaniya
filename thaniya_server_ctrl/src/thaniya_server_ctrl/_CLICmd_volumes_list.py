

import os
import shutil

import jk_utils
import jk_argparsing
import jk_mounting
import jk_console

from thaniya_server.app.CLICmdBase import CLICmdBase
from thaniya_server.app.CLICmdParams import CLICmdParams
from thaniya_server_archive.volumes import Device
from thaniya_server_archive.volumes import BackupVolumeID
from thaniya_server_archive.volumes import BackupVolumeInfo
from thaniya_server_archive.volumes import BackupVolumeManager

from .AppRuntimeServerCtrl import AppRuntimeServerCtrl
from .TextDiskSpaceGraphGenerator import TextDiskSpaceGraphGenerator

FG = jk_console.Console.ForeGround







class _CLICmd_volumes_list(CLICmdBase):

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
		return "vol-ls"
	#

	#
	# The short description.
	#
	@property
	def shortDescription(self) -> str:
		return "List all volumes."
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
	#

	def _runImpl(self, p:CLICmdParams) -> bool:
		with p.out.section("List volumes") as out:

			table = jk_console.SimpleTable()
			table.addRow(
				"Backup Volume ID",
				"Volume Cfg Type",
				"Device",
				"Device Type",
				"Mount Point",
				"Backup Base Dir Path",
				"File System",
				"Bytes Total",
				"Bytes Free",
				"PhySecSize",
				"Valid",
				"Active",
				).hlineAfterRow = True
			table.row(0).color = FG.STD_WHITE

			for bvi in self.__appRuntime.backupVolumeMgr.listVolumes(p.log):
				assert isinstance(bvi, BackupVolumeInfo)
				row = table.addRow(
					bvi.backupVolumeID.hexData,
					bvi.volumeCfgType,
					bvi.device.devType,
					bvi.device.devPath,
					bvi.device.mountPoint,
					bvi.backupBaseDirPath,
					bvi.device.fsType,
					jk_utils.formatBytes(bvi.device.sizeInBytes),
					jk_utils.formatBytes(bvi.device.bytesFree),
					str(bvi.device.phySecSizeInBytes),
					"yes" if bvi.isValid else "no",
					"yes" if bvi.isActive else "no",
				)
				if not bvi.isValid:
					row.color = FG.STD_LIGHTRED
				elif bvi.isActive:
					row.color = FG.STD_LIGHTGREEN
				else:
					row.color = FG.STD_DARKGRAY

			p.out.printTable(table)

	#

#





