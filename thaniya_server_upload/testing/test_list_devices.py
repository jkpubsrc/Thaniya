#!/usr/bin/python3




import os

import jk_json

import thaniya_server.volumes




print()
print("-" * 160)
print()

for x in thaniya_server.volumes.DeviceIterator.listMountedDevices():
	x.dump()

print()
print("-" * 160)
print()

for x in thaniya_server.volumes.DeviceIterator.listNonMountedDevices():
	x.dump()

print()
print("-" * 160)
print()





# identify:
#	(type = "part") and (fstype != null) and (mountpoint != null)				=> mounted partition
#	(type = "part") and (fstype != null) and (mountpoint == null)				=> partition not mounted
#	(type = "rom")											=> unusable, as this is a cdrom or similar
#	(type = "loop") and (fstype != null) and (mountpoint != null)				=> loop device mounted
#																					-> mountpoint should not start with "/snap/"
#	(type = "loop") and (fstype == "crypto_LUKS") and (mountpoint != null)		=> mounted LUKS device
#	(type = "loop") and (fstype == "crypto_LUKS") and (mountpoint == null)		=> LUKS device not mounted



#jk_json.prettyPrint(jk_sysinfo.get_lsblk())




