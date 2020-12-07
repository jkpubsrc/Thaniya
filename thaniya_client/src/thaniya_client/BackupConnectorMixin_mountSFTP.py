


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
class BackupConnectorMixin_mountSFTP(object):

	SSHFS_PATH = "/usr/bin/sshfs"

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def _mountSSH(self, localDirPath:str, sshHostAddress:str, sshPort:int, sshLogin:str, sshPassword:str, sshDirPath:str) -> bool:
		assert isinstance(localDirPath, str)
		assert os.path.isdir(localDirPath)
		localDirPath = os.path.abspath(localDirPath)

		mounter = jk_mounting.Mounter()
		mip = mounter.getMountInfoByMountPoint(localDirPath)
		if mip is not None:
			raise Exception("Directory " + repr(localDirPath) + " already used by mount!")

		cmd = [
			BackupConnectorMixin_mountSFTP.SSHFS_PATH,
			"-p", str(sshPort), "-o", "password_stdin", "-o", "reconnect", sshLogin + "@" + sshHostAddress + ":" + sshDirPath, localDirPath
		]

		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		p.stdin.write((sshPassword + "\n").encode("utf-8"))
		(stdout, stderr) = p.communicate(timeout=3)
		if p.returncode != 0:
			returnCode1 = p.returncode
			stdOutData1 = stdout.decode("utf-8")
			stdErrData1 = stderr.decode("utf-8")
			p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			p.stdin.write(("yes\n" + sshPassword + "\n").encode("utf-8"))
			(stdout, stderr) = p.communicate(timeout=3)
			if p.returncode != 0:
				returnCode2 = p.returncode
				stdOutData2 = stdout.decode("utf-8")
				stdErrData2 = stderr.decode("utf-8")
				print("Mount attempt 1:")
				print("\tcmd =", cmd)
				print("\treturnCode =", returnCode1)
				print("\tstdOutData =", repr(stdOutData1))
				print("\tstdErrData =", repr(stdErrData1))
				print("Mount attempt 2:")
				print("\treturnCode =", returnCode2)
				print("\tstdOutData =", repr(stdOutData2))
				print("\tstdErrData =", repr(stdErrData2))
				raise Exception("Failed to mount device!")
				return False
			else:
				return True
		else:
			return True
	#

#












