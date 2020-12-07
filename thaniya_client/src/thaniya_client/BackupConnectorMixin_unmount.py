


import time
import os
import subprocess
import typing

import jk_mounting
import jk_typing

from .AbstractBackupConnector import AbstractBackupConnector
from .ThaniyaIO import ThaniyaIO
from .ThaniyaBackupContext import ThaniyaBackupContext








#
# NOTE: For this connector to work the user running this program needs to have <c>sudo</c> rights for invoking <c>umount</c>.
#
class BackupConnectorMixin_unmount(object):

	SUDO_PATH = "/usr/bin/sudo"
	UMOUNT_PATH = "/bin/umount"

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def _tryRepeatedUnmount(self, localDirPath:str, nRepeats:int) -> typing.Union[Exception,None]:
		assert isinstance(localDirPath, str)
		assert isinstance(nRepeats, int)
		assert nRepeats > 0

		lastException = None
		for i in range(0, nRepeats):
			time.sleep(1)
			try:
				self._umount(localDirPath)
				return None
			except Exception as ee:
				lastException = ee

		return lastException
	#

	def _umount(self, localDirPath:str, throwExceptionOnError:bool = True) -> bool:
		assert isinstance(localDirPath, str)
		assert isinstance(throwExceptionOnError, bool)

		cmd = [
			BackupConnectorMixin_unmount.SUDO_PATH,
			BackupConnectorMixin_unmount.UMOUNT_PATH,
			localDirPath,
		]
		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(stdout, stderr) = p.communicate(timeout=10)
		if p.returncode != 0:
			returnCode = p.returncode
			stdOutData = stdout.decode("utf-8")
			stdErrData = stderr.decode("utf-8")
			print("Unmount attempt:")
			print("\treturnCode =", returnCode)
			print("\tstdOutData =", repr(stdOutData))
			print("\tstdErrData =", repr(stdErrData))
			if throwExceptionOnError:
				raise Exception("Failed to umount device!")
			return False
		else:
			return True
	#

#












