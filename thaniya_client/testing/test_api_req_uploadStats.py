#!/usr/bin/python3


from _testprg import *

import thaniya_client.server
import thaniya_client.cfg










with testPrg(__file__, hasDataDir=False, hasTempDir=False) as (ioCtx, dataDirPath, tempDirPath, log):

	cfg = jk_json.load("cfg-test-api.jsonc")

	api = thaniya_client.server.ThaniyaServerAPIConnectorV1(cfg["HOSTNAME"], cfg["UPLOAD_HTTP_PORT"])

	api.authenticate(cfg["LOGIN"], cfg["PASSWORD"])
	jk_json.prettyPrint(api.uploadStats())
	
	print()








