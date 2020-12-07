


import time
import typing
import collections

import jk_typing







_Resp = collections.namedtuple("_Resp", [ "serverData", "clientData" ])




@jk_typing.checkFunctionSignature()
def _checkBytesEqual(someBytesA:bytes, someBytesB:bytes, nExpected:int):
	lenA = len(someBytesA)
	assert lenA > 0
	lenB = len(someBytesB)
	assert lenB > 0

	bEqual = True
	for i in range(0, nExpected):
		vA = someBytesA[i % lenA]
		vB = someBytesB[i % lenB]
		if vA != vB:
			bEqual = False

	time.sleep(0.01)

	if (lenA != nExpected) or (lenB != nExpected) or not bEqual:
		return False

	return True
#
















