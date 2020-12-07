#!/usr/bin/python3




import os

import jk_simpleobjpersistency

import thaniya_server.usermgr
import thaniya_server.sysusers
import thaniya_server.slots





os.makedirs("data", exist_ok=True)

persistencyMgr = jk_simpleobjpersistency.PersistencyManager2("data")

backupUserMgr = thaniya_server.usermgr.BackupUserManager(persistencyMgr)

sudoScriptRunner = thaniya_server.sysusers.SudoScriptRunner("/etc/thaniya/sudoscripts")

uploadSlotMgr = thaniya_server.slots.UploadSlotManager(backupUserMgr, sudoScriptRunner, persistencyMgr)











