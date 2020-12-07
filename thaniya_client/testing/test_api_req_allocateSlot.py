#!/usr/bin/python3




from _testprg import *

import thaniya_client.server
import thaniya_client.cfg





with testPrg(__file__, hasDataDir=False, hasTempDir=False) as (ioCtx, dataDirPath, tempDirPath, log):

	api = thaniya_client.server.ThaniyaServerAPIConnectorV1("localhost", 9002)

	api.authenticate("foo", "64563d1146a7b045360bb15901ef0aa3826ae6f4a66ec3869921a3b772d10614")

	nEstimatedTotalBytesToUpload = jk_utils.AmountOfBytes("5M")		# upload 5 MByte of data

	ret = api.allocateSlot(
		estimatedTotalBytesToUpload=int(nEstimatedTotalBytesToUpload)
	)
	jk_json.prettyPrint(ret)
	
	print()








