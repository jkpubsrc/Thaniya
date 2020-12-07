#!/usr/bin/python3




import os
import hashlib

import jk_simpleobjpersistency

import thaniya_server.usermgr





os.makedirs("data", exist_ok=True)

pm = jk_simpleobjpersistency.PersistencyManager2("data")

backupUserMgr = thaniya_server.usermgr.BackupUserManager(pm)



userName = "foo"
passwordHash = hashlib.sha256("bar".encode("utf-8")).hexdigest()
eMail = "foo@bar"
role = "backup"
comment = None



backupUserMgr.createUser(userName, passwordHash, eMail, role, comment)

for u in backupUserMgr.users:
	u.dump()












