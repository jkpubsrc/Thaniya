


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
class BackupConnectorMixin_mountCIFS(object):

	#SMB_CLIENT_PATH = "/usr/bin/smbclient"
	MOUNT_PATH = "/bin/mount"

	################################################################################################################################
	## Constructor
	################################################################################################################################

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def _mountCIFS(self,
		ctx:ThaniyaBackupContext,
		localDirPath:str,
		cifsHostAddress:str,
		#cifsPort:int,
		cifsShareName:str,
		cifsLogin:str,
		cifsPassword:str,
		cifsVersion:str) -> bool:

		assert isinstance(localDirPath, str)
		assert os.path.isdir(localDirPath)
		localDirPath = os.path.abspath(localDirPath)

		mounter = jk_mounting.Mounter()
		mip = mounter.getMountInfoByMountPoint(localDirPath)
		if mip is not None:
			raise Exception("Directory " + repr(localDirPath) + " already used by mount!")

		credentialFilePath = ctx.privateTempDir.writeTextFile(
			"username=" + cifsLogin + "\npassword=" + cifsPassword + "\n"
			)

		options = [
			"user=",
			cifsLogin,
			",credentials=",
			credentialFilePath,
			",rw",
		]
		if cifsVersion:
			options.append(",vers=")
			options.append(cifsVersion)

		cmd = [
			BackupConnectorMixin_mountCIFS.MOUNT_PATH,
			"-t", "cifs",
			"-o", "".join(options),
			"//" + cifsHostAddress + "/" + cifsShareName,
			localDirPath,
		]
		# print(" ".join(cmd))

		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		p.stdin.write((cifsPassword + "\n").encode("utf-8"))
		(stdout, stderr) = p.communicate(timeout=3)
		if p.returncode != 0:
			returnCode1 = p.returncode
			stdOutData1 = stdout.decode("utf-8")
			stdErrData1 = stderr.decode("utf-8")
			print("Mount attempt:")
			print("\tcmd =", cmd)
			print("\treturnCode =", returnCode1)
			print("\tstdOutData =", repr(stdOutData1))
			print("\tstdErrData =", repr(stdErrData1))
			raise Exception("Failed to mount device!")
			return False
		else:
			return True
	#

#












