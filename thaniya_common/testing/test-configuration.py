#!/usr/bin/python3



from _testprg import *

from thaniya_common.cfg import *
from ExampleCfg import ExampleCfg

"""

This file allows testing the implementation of the base classes that assist in implementing JSON file based configurations and information files.

"""






with testPrg(__file__, hasDataDir=True) as (ioCtx, dataDirPath, tempDirPath, log):

	filePath = os.path.join(dataDirPath, "sample-cfg.jsonc")

	with open(filePath, "r") as f:
		jData = jk_json.load(f)
		jData["magic"]["comment"] = None
		rawOrg = jk_json.dumps(jData, indent="\t", sort_keys=True)

	cfg = ExampleCfg.loadFromFile(filePath)
	cfg.dump()

	print()
	print()
	print()

	rawAfterLoad = jk_json.dumps(cfg.toJSON(), indent="\t", sort_keys=True)

	print("=" * 120)
	print(rawOrg)
	print("=" * 120)
	print(rawAfterLoad)
	print("=" * 120)

	assert rawOrg == rawAfterLoad






