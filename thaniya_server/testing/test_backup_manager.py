#!/usr/bin/python3




import os
import sys

import jk_json
import jk_logging

from thaniya_server.volumes import *





log = jk_logging.ConsoleLogger.create(logMsgFormatter = jk_logging.COLOR_LOG_MESSAGE_FORMATTER)
try:





	mgr = BackupVolumeManager(log)

	"""
	for o in mgr.backupVolumesOpen:
		o.dump()

	for o in mgr.backupVolumeIDs:
		print(o)

	volume = mgr.openDirectoryVolume("BackupVolumeID(<d0df2264383a28eda737d13b5944b051>)")
	assert isinstance(volume, thaniya_server.volumes.BackupVolume)
	"""

	#mgr.createDirectoryVolume("/tmp/THANIYA_BACKUP_TEST2")

	#mgr.activateVolume(BackupVolumeID.parseFromStr("BackupVolumeID(<d0df2264383a28eda737d13b5944b051>)"))
	#mgr.activateVolume("3c35dec5742347f9f9ccb69c2e46acc1")

	for v in mgr.listVolumes():
		v.dump()


	log.success("Success!")

except jk_logging.ExceptionInChildContextException as ee:
	pass
except Exception as ee:
	log.error(ee)
	sys.exit(1)


#os.makedirs("/tmp/THANIYA_BACKUP_TEST1", exist_ok=True)
#bid = mgr.createDirectoryVolume("/tmp/THANIYA_BACKUP_TEST1")
#assert isinstance(bid, thaniya_server.volumes.BackupVolumeID)











#backupDevice = mgr.tryOpenFromDevice("/")

#backupDevice.dump()





# identify:
#	(type = "part") and (fstype != null) and (mountpoint != null)				=> mounted partition
#	(type = "part") and (fstype != null) and (mountpoint == null)				=> partition not mounted
#	(type = "rom")											=> unusable, as this is a cdrom or similar
#	(type = "loop") and (fstype != null) and (mountpoint != null)				=> loop device mounted
#																					-> mountpoint should not start with "/snap/"
#	(type = "loop") and (fstype == "crypto_LUKS") and (mountpoint != null)		=> mounted LUKS device
#	(type = "loop") and (fstype == "crypto_LUKS") and (mountpoint == null)		=> LUKS device not mounted



#jk_json.prettyPrint(jk_sysinfo.get_lsblk())




