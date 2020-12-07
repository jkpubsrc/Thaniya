#!/usr/bin/python3




from _testprg import *

from thaniya_server_sudo import *







with testPrg(__file__) as (ioCtx, dataDirPath, tempDirPath, log):

	sudoScriptRunner = SudoScriptRunner("/etc/thaniya/sudoscripts")

	r = sudoScriptRunner.run1("script_test1", "01", None, None)
	r.dump(printFunc=log.notice)

	assert isinstance(r, SudoScriptResult)
	assert r.returnCode == 0
	assert r.isSuccess
	assert not r.isError
	assert r.errorID is None
	assert len(r.stdOutLines) == 3
	assert r.stdOutLines[0] == "TEST :: THANIYA_ACCOUNT = thaniya_01"
	assert r.stdOutLines[2] == "TEST :: uid=0(root) gid=0(root) groups=0(root)"
	assert len(r.stdErrLines) == 0

	log.success("Success!")









