#!/usr/bin/python3



import typing
import os
import sys
import time

import shutil

import jk_json
import jk_utils
import jk_logging

from thaniya_common.utils import IOContext
from thaniya_common import UploadedBackupInfoFile









ioCtx = IOContext()

dirPath = os.path.abspath(os.path.splitext(os.path.basename(__file__))[0])

if os.path.isdir(dirPath):
	shutil.rmtree(dirPath)

ioCtx.ensureDirExists(dirPath)









with jk_logging.wrapMain() as log:

	filePath = os.path.join(dirPath, "_upload_info.json")

	f = UploadedBackupInfoFile()
	f.setValue("tBackupStart", jk_utils.TimeStamp.now())
	f.setValue("tBackupEnd", jk_utils.TimeStamp.now())
	f.setValue("sizeInBytes", jk_utils.AmountOfBytes(12345))
	f.writeToFile(filePath)

	f2 = UploadedBackupInfoFile.loadFromFile(filePath)
	f2.dump()












