#!/usr/bin/python3




from _testprg import *

from thaniya_server_sudo import *







with testPrg(__file__) as (ioCtx, dataDirPath, tempDirPath, log):

	sudoScriptRunner = SudoScriptRunner("/etc/thaniya/sudoscripts")

	print("Available scripts:")
	for scriptName in sudoScriptRunner.scriptNames:
		print("\t" + scriptName)









