#!/usr/bin/python3


"""
import os

import jk_utils
import jk_pwdinput
import jk_logging
import jk_json

from thaniya_client import *
from thaniya_client.tasks import *





cfg = jk_json.loadFromFile("../cfg-cifs.jsonc")





if not cfg["ssh_password"]:
	cfg["ssh_password"] = jk_pwdinput.readpwd("Connection password for user " + cfg["ssh_login"] + ": ")

log = jk_logging.ConsoleLogger.create(logMsgFormatter=jk_logging.COLOR_LOG_MESSAGE_FORMATTER)
try:

	driver = ThaniyaBackupDriver(
		backupConnector = thaniya_client.BackupConnector_CIFSMount(),
		backupConnectorParameters = cfg,
		targetDirStrategy = TargetDirectoryStrategy_DateDefault(),
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

except ProcessingFallThroughError as ee:
	pass
except jk_logging.ExceptionInChildContextException as ee:
	pass
except Exception as ee:
	log.error(ee)
"""



