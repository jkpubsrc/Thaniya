
import os

import jk_utils
import jk_pwdinput

from .AbstractBackupConnector import AbstractBackupConnector
from .BackupConnector_CIFSMount import BackupConnector_CIFSMount
from .BackupConnector_SFTPMount import BackupConnector_SFTPMount
from .BackupConnector_Local import BackupConnector_Local
from .BackupConnector_ThaniyaSFTPMount import BackupConnector_ThaniyaSFTPMount
from .AbstractTargetDirectoryStrategy import AbstractTargetDirectoryStrategy
from .TargetDirectoryStrategy_DateDefault import TargetDirectoryStrategy_DateDefault
from .TargetDirectoryStrategy_StaticDir import TargetDirectoryStrategy_StaticDir
from .ThaniyaBackupDriver import ThaniyaBackupDriver
from .ThaniyaClientCfg import ThaniyaClientCfg










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
			targetDirStrategy = TargetDirectoryStrategy_DateDefault(),
		)

		return driver
	#

	@staticmethod
	def newSimpleThaniyaMount(
		thaniya_host:str = None,
		thaniya_login:str = None,
		thaniya_apiPassword:str = None,
		thaniya_port:str = None) -> ThaniyaBackupDriver:

		if (thaniya_host is None) and (thaniya_port is None) and (thaniya_login is None) and (thaniya_apiPassword is None):
			cfg = ThaniyaClientCfg.load()
			p = {
				"thaniya_host": cfg.server["host"],
				"thaniya_port": cfg.server["port"],
				"thaniya_login": cfg.server["login"],
				"thaniya_apiPassword": cfg.server["apiPassword"],
			}
		else:
			p = {
				"thaniya_host": thaniya_host,
				"thaniya_port": thaniya_port,
				"thaniya_login": thaniya_login,
				"thaniya_apiPassword": thaniya_apiPassword,
			}

		if not p["thaniya_host"]:
			raise ValueError("thaniya_host")
		if not p["thaniya_port"]:
			raise ValueError("thaniya_port")
		if not p["thaniya_login"]:
			raise ValueError("thaniya_login")
		if not p["thaniya_apiPassword"]:
			raise ValueError("thaniya_apiPassword")

		driver = ThaniyaBackupDriver(
			backupConnector = BackupConnector_ThaniyaSFTPMount(),
			backupConnectorParameters = p,
			targetDirStrategy = TargetDirectoryStrategy_StaticDir("upload"),			# all uploads *must* go to this subdirectory!
		)

		return driver
	#

#








