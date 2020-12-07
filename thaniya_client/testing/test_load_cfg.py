#!/usr/bin/python3





import jk_logging

import thaniya_client.cfg





with jk_logging.wrapMain() as log:


	print()

	cfg = thaniya_client.cfg.ThaniyaClientCfg.load(log)

	print(cfg.getValue("general", "tempBaseDir"))

	print()








