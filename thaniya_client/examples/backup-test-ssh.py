#!/usr/bin/python3




from thaniya_client import *




# define the server's backup parameters

REMOTE_USERNAME = "woodoo"
REMOTE_HOST = "192.168.10.100"
REMOTE_DESTINATION_BASE_PATH = "/mounts/phy/sda1/BACKUPS-THANIYA/woodoo"
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







