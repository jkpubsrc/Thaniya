#!/usr/bin/python3




from _testprg import *

from thaniya_server_sudo import *

import thaniya_server_upload







with testPrg(__file__) as (ioCtx, dataDirPath, tempDirPath, log):

	resultDir = thaniya_server_upload.UploadHttpdCfg.load().slotMgr.getValue("resultDir")

	sudoScriptRunner = SudoScriptRunner("/etc/thaniya/sudoscripts")

	r = sudoScriptRunner.run1("script_test4", "01", None, None)
	r.dump(printFunc=log.notice)

	assert isinstance(r, SudoScriptResult)
	assert r.returnCode == 0
	assert r.isSuccess
	assert not r.isError
	assert r.errorID is None
	assert len(r.stdOutLines) == 4
	assert r.stdOutLines[0] == "TEST :: THANIYA_ACCOUNT = thaniya_01"
	assert r.stdOutLines[2] == "TEST :: RESULT_DIR = " + resultDir
	assert r.stdOutLines[3] == "TEST :: uid=0(root) gid=0(root) groups=0(root)"

	log.success("Success!")






