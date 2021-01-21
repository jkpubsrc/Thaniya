#!/usr/bin/python3


import os

import jk_utils
import jk_logging

from thaniya_client import *
from thaniya_client.tasks import *







# define the server's backup parameters

REMOTE_USERNAME = "someuser"
REMOTE_API_PASSWORD = "aabbccddeeff00112233445566778899"
REMOTE_HOST = "somehost"
REMOTE_PORT = 22







with jk_logging.wrapMain() as log:

	homeDir = jk_utils.users.getUserHome()

	# obtain a backup driver to use

	driver = ThaniyaFactory.newSimpleThaniyaMount(
		thaniya_host = REMOTE_HOST,
		thaniya_login = REMOTE_USERNAME,
		thaniya_apiPassword = REMOTE_API_PASSWORD,
		thaniya_port = REMOTE_PORT,
	)

	# perform the backup

	driver.performBackup(
		backupIdentifier = "home-config-dir",
		backupTasks = [
			TBackupDir(
				sourceDirPath = os.path.join(homeDir, ".config"),
			),
		],
	)







