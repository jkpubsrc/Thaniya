#!/usr/bin/python3



from thaniya_common.utils import *
from _testprg import *




with testPrg(__file__, hasDataDir=False) as (ioCtx, dataDirPath, tempDirPath, log):

	p = APIPassword.generate()
	print("    repr: ", repr(p))
	print("     HEX: ", p.toHexStr())
	print("  BASE64: ", p.toBase64Str())

	p1 = APIPassword(p.toHexStr())
	p2 = APIPassword(p.toBase64Str())
	assert p1 == p
	assert p2 == p
	assert p1 == p2

	log.success("Success.")





