#!/usr/bin/python3




import os

import jk_simpleobjpersistency

import thaniya_server.usermgr





os.makedirs("data", exist_ok=True)

pm = jk_simpleobjpersistency.PersistencyManager2("data")

backupUserMgr = thaniya_server.usermgr.BackupUserManager(pm)

for u in backupUserMgr.users:
	u.dump()












