#!/usr/bin/python3


from _testprg import *

from thaniya_client import *
from thaniya_client.tasks import *










with testPrg(__file__, hasDataDir=False, hasTempDir=False) as (ioCtx, dataDirPath, tempDirPath, log):

	cfg = jk_json.load("cfg-test-api.jsonc")

	driver = ThaniyaBackupDriver(
		backupConnector = BackupConnector_ThaniyaSFTPMount(),
		backupConnectorParameters = {
			"thaniya_serverLogin": cfg["LOGIN"],
			"thaniya_serverPassword": cfg["PASSWORD"],
			"thaniya_serverHost": cfg["HOSTNAME"],
			"thaniya_serverPort": cfg["UPLOAD_HTTP_PORT"],
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








