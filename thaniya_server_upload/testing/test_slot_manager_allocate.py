#!/usr/bin/python3




import os

import jk_logging
import jk_simpleobjpersistency
import jk_json

import thaniya_server.usermgr
import thaniya_server.sysusers
import thaniya_server.slots



with jk_logging.wrapMain() as log:

	os.makedirs("data", exist_ok=True)

	persistencyMgr = jk_simpleobjpersistency.PersistencyManager2("data")

	backupUserMgr = thaniya_server.usermgr.BackupUserManager(persistencyMgr)
	backupUser = backupUserMgr.getUser("foo")
	assert backupUser

	sudoScriptRunner = thaniya_server.sysusers.SudoScriptRunner("/etc/thaniya/sudoscripts")

	uploadSlotMgr = thaniya_server.slots.UploadSlotManager(backupUserMgr, sudoScriptRunner, persistencyMgr)

	slotData = uploadSlotMgr.tryAllocateSlot(backupUser, log)
	jk_json.prettyPrint(slotData)










