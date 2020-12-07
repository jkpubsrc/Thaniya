#!/usr/bin/python3


from _testprg import *

from thaniya_client import *
from thaniya_client.tasks import *





LOGIN = "foo"
PASSWORD = "64563d1146a7b045360bb15901ef0aa3826ae6f4a66ec3869921a3b772d10614"
HOSTNAME = "localhost"
UPLOAD_HTTP_PORT = 9002







with testPrg(__file__, hasDataDir=False, hasTempDir=False) as (ioCtx, dataDirPath, tempDirPath, log):

	driver = ThaniyaBackupDriver(
		backupConnector = BackupConnector_ThaniyaSFTPMount(),
		backupConnectorParameters = {
			"thaniya_serverLogin": LOGIN,
			"thaniya_serverPassword": PASSWORD,
			"thaniya_serverHost": HOSTNAME,
			"thaniya_serverPort": UPLOAD_HTTP_PORT,
		},
		targetDirStrategy = TargetDirectoryStrategy_StaticDir("upload"),			# all uploads *must* go to this subdirectory!
	)

	driver.performBackup(
		backupIdentifier = "fooBarXYZ",
		backupTasks = [
			TBackupDir(
				sourceDirPath="/etc",
			),
		],
		#bSimulate = False
	)








