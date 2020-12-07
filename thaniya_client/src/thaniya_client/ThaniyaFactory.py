
import os

import jk_utils
import jk_pwdinput

from .AbstractBackupConnector import AbstractBackupConnector
from .BackupConnector_CIFSMount import BackupConnector_CIFSMount
from .BackupConnector_SFTPMount import BackupConnector_SFTPMount
from .BackupConnector_Local import BackupConnector_Local
from .AbstractTargetDirectoryStrategy import AbstractTargetDirectoryStrategy
from .TargetDirectoryStrategy_DateDefault import TargetDirectoryStrategy_DateDefault
from .TargetDirectoryStrategy_StaticDir import TargetDirectoryStrategy_StaticDir
from .ThaniyaBackupDriver import ThaniyaBackupDriver











class ThaniyaFactory(object):

	@staticmethod
	def newSimpleSSHMount(
		ssh_hostAddress:str,
		ssh_login:str,
		ssh_password:str,
		ssh_port:str,
		ssh_dirPath:str) -> ThaniyaBackupDriver:

		if not ssh_password:
			ssh_password = jk_pwdinput.readpwd("Connection password for " +  ssh_login + "@" +  ssh_hostAddress + " : ")
			if not ssh_password:
				return None

		driver = ThaniyaBackupDriver(
			backupConnector = BackupConnector_SFTPMount(),
			backupConnectorParameters = {
				"ssh_hostAddress": ssh_hostAddress,
				"ssh_login": ssh_login,
				"ssh_password": ssh_password,
				"ssh_port": ssh_port,
				"ssh_dirPath": ssh_dirPath,
			},
			mountDirPath = None,
			ensureMountDirExists = True,
			targetDirStrategy = TargetDirectoryStrategy_DateDefault(),
		)

		return driver
	#

	@staticmethod
	def newSimpleLocal(
		local_dirPath:str) -> ThaniyaBackupDriver:

		driver = ThaniyaBackupDriver(
			backupConnector = BackupConnector_Local(),
			backupConnectorParameters = {
			},
			mountDirPath = local_dirPath,
			ensureMountDirExists = False,
			targetDirStrategy = TargetDirectoryStrategy_DateDefault(),
		)

		return driver
	#

#








