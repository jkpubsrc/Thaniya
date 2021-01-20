#!/usr/bin/python3



import os
import json
import typing
import sys
import time

import jk_json
import jk_utils
import jk_logging
import jk_typing
from jk_testing import Assert
import jk_console

from thaniya_common.utils import IOContext






def testPrg(sourceFilePath:str, hasDataDir:bool = False, hasTempDir:bool = False):

	class _LogCtx(object):

		def __init__(self, ioCtx, dataDirPath, tempDirPath, log):
			self.ioCtx = ioCtx
			self.dataDirPath = dataDirPath
			self.tempDirPath = tempDirPath
			self.log = log
		#

		def __enter__(self):
			return self.ioCtx, self.dataDirPath, self.tempDirPath, self.log
		#

		def __exit__(self, ex_type, ex_value, ex_traceback):
			if ex_type != None:
				if ex_type == SystemExit:
					return False
				if not isinstance(ex_value, jk_logging.ExceptionInChildContextException):
					self.log.error(ex_value)
				sys.exit(1)
	
			return True
		#

	#

	log = jk_logging.ConsoleLogger.create(logMsgFormatter=jk_logging.COLOR_LOG_MESSAGE_FORMATTER)

	ioCtx = IOContext()

	if hasDataDir:
		dataDirPath = os.path.abspath("_" + os.path.splitext(os.path.basename(sourceFilePath))[0] + ".sav")
		if not os.path.isdir(dataDirPath):
			raise Exception("No such directory: " + os.path.basename(dataDirPath))
	else:
		dataDirPath = None

	if hasTempDir:
		tempDirPath = os.path.abspath("_" + os.path.splitext(os.path.basename(sourceFilePath))[0] + ".dir")
		if os.path.isdir(tempDirPath):
			shutil.rmtree(tempDirPath)
		ioCtx.ensureDirExists(tempDirPath)
	else:
		tempDirPath = None

	return _LogCtx(ioCtx, dataDirPath, tempDirPath, log)

#






