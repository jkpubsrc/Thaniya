#!/usr/bin/python3




from _testprg import *

from thaniya_server_sudo import *







with testPrg(__file__) as (ioCtx, dataDirPath, tempDirPath, log):

	sudoScriptRunner = SudoScriptRunner("/etc/thaniya/sudoscripts")

	r = sudoScriptRunner.run1("script_test3", "01", None, None)
	r.dump(printFunc=log.notice)

	assert isinstance(r, SudoScriptResult)
	assert r.returnCode == 1
	assert not r.isSuccess
	assert r.isError
	assert r.errorID == "errFooBar"
	assert len(r.stdOutLines) == 1
	assert len(r.stdErrLines) == 0

	log.success("Success!")






