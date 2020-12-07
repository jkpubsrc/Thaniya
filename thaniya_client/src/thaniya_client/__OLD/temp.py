

import os
import random
import string
import typing
import tempfile

import jk_utils




def writeTempFile(fileMode:typing.Union[jk_utils.ChModValue,int,str], text:str) -> str:
	assert isinstance(text, str)

	if isinstance(fileMode, jk_utils.ChModValue):
		pass
	elif isinstance(fileMode, (int, str)):
		fileMode = jk_utils.ChModValue(fileMode)
	else:
		raise Exception("File mode must be int, str or jk_utils.ChModValue!")

	# ----

	characters = string.ascii_letters + string.digits
	nLength = 32
	baseFilePath = "/tmp/"

	filePath = None
	while True:
		filePath = baseFilePath + "".join(random.choice(characters) for i in range(0, nLength))
		if not os.path.exists(filePath):
			break

	with open(os.open(filePath, os.O_CREAT | os.O_WRONLY, fileMode.toInt()), "w") as f:
		f.write(text)
	
	return filePath
#


