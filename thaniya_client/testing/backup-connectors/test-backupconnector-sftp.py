#!/usr/bin/python3


import os

import jk_utils
import jk_pwdinput
import jk_logging
import jk_json

from thaniya_client import *
from thaniya_client.tasks import *





cfg = jk_json.loadFromFile("../cfg-sftp.jsonc")





if not cfg["ssh_password"]:
	cfg["ssh_password"] = jk_pwdinput.readpwd("Connection password for user " + cfg["ssh_login"] + ": ")

with jk_logging.wrapMain() as log:

	driver = ThaniyaBackupDriver(
		backupConnector = BackupConnector_SFTPMount(),
		backupConnectorParameters = cfg,
		targetDirStrategy = TargetDirectoryStrategy_DateDefault(),
	)

	driver.testConnector("fooBar")





