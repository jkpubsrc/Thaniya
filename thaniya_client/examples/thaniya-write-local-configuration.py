#!/usr/bin/python3


import jk_logging

from thaniya_client import *
from thaniya_client.tasks import *









with jk_logging.wrapMain() as log:

	cfg = ThaniyaClientCfg()

	cfg.server["host"] = "somehost"
	cfg.server["port"] = 9002
	cfg.server["login"] = "someuser"
	cfg.server["apiPassword"] = "aabbccddeeff00112233445566778899"

	cfgFilePath = cfg.writeToLocal()
	log.success("The configuration has been written to: " + cfgFilePath)






