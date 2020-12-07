#!/usr/bin/python3


import os

import jk_utils
import jk_pwdinput
import jk_logging

from thaniya_client import *
from thaniya_client.tasks import *




LOCAL_MOUNT_DIR_PATH = os.path.abspath("tmp2")
os.makedirs(LOCAL_MOUNT_DIR_PATH, exist_ok=True)




with jk_logging.wrapMain() as log:

	driver = ThaniyaBackupDriver(
		backupConnector = BackupConnector_Local(),
		backupConnectorParameters = {
			"dirPath": LOCAL_MOUNT_DIR_PATH,
		},
		targetDirStrategy = TargetDirectoryStrategy_None(),
		#targetDirStrategy = TargetDirectoryStrategy_DateDefault(),
	)

	driver.performBackup(
		backupIdentifier = "fooBar",
		backupTasks = [
			TBackupDir(
				sourceDirPath="/etc",
			),
		],
		#bSimulate = False
	)




