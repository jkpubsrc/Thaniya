#!/usr/bin/python3




from thaniya_client import *
from thaniya_client.tasks import *




# define the server's backup parameters

REMOTE_USERNAME = "someuser"
REMOTE_HOST = "somehost"
REMOTE_DESTINATION_BASE_PATH = "/path/to/backup/main"
REMOTE_PORT = 22






# obtain a backup driver

driver = ThaniyaFactory.newSimpleSSHMount(
	ssh_hostAddress = REMOTE_HOST,
	ssh_login = REMOTE_USERNAME,
	ssh_password = None,
	ssh_port = REMOTE_PORT,
	ssh_dirPath = REMOTE_DESTINATION_BASE_PATH,
)

# perform the backup

driver.performBackup(
	backupIdentifier = "test",
	backupTasks = [
		TBackupDir(
			sourceDirPath = "/etc/init.d",
		),
	],
	bSimulate=False
)







