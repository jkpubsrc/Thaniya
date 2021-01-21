#!/usr/bin/python3


import os

import jk_utils
import jk_logging

from thaniya_client import *
from thaniya_client.tasks import *









with jk_logging.wrapMain() as log:

	homeDir = jk_utils.users.getUserHome()

	# obtain a backup driver to use

	driver = ThaniyaFactory.newSimpleThaniyaMount()

	# perform the backup

	driver.performBackup(
		backupIdentifier = "home-config-dir",
		backupTasks = [
			TBackupDir(
				sourceDirPath = os.path.join(homeDir, ".config"),
			),
		],
	)












