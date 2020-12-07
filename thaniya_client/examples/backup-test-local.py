#!/usr/bin/python3




from thaniya_client import *




# define the server's backup parameters

BACKUP_STORAGE_PATH = "/path/to/backup/main"






# obtain a backup driver

driver = ThaniyaFactory.newSimpleLocal(
	local_dirPath = BACKUP_STORAGE_PATH,
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







