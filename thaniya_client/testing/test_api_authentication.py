#!/usr/bin/python3


from _testprg import *

import thaniya_client.server
import thaniya_client.cfg





with testPrg(__file__, hasDataDir=False, hasTempDir=False) as (ioCtx, dataDirPath, tempDirPath, log):

	#cfg = thaniya_client.cfg.ThaniyaClientCfg.load(log)
	#print(cfg.getValue("general", "tempBaseDir"))

	api = thaniya_client.server.ThaniyaServerAPIConnectorV1("localhost", 9002)
	
	#api.noopAuth()

	api.noop()

	api.authenticate("foo", "64563d1146a7b045360bb15901ef0aa3826ae6f4a66ec3869921a3b772d10614")

	api.noopAuth()

	while True:
		time.sleep(10)
		api.noopAuth()
	
	print()








