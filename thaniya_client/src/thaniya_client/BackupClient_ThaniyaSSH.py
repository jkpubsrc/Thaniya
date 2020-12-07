

import sys
import os
import json
import urllib.request
import urllib.parse
import requests
import subprocess
from furl import furl

import jk_json
import jk_mounting


from .AbstractBackupConnector import AbstractBackupConnector
from .ThaniyaServerConnector import ThaniyaServerConnector




#
# Objects of this class are instantiated by ShiroiBackup.
#
class BackupClient_ThaniyaSSH(AbstractBackupConnector):

	SSHFS_PATH = "/usr/bin/sshfs"
	SUDO_PATH = "/usr/bin/sudo"
	UMOUNT_PATH = "/bin/umount"

	def __init__(self, connector:ThaniyaServerConnector, initStructure:dict):
		assert isinstance(connector, ThaniyaServerConnector)
		assert isinstance(initStructure, dict)

		if not os.path.isfile(BackupClient_ThaniyaSSH.SSHFS_PATH):
			raise Exception("sshfs is required but it is not installed!")

		self.__connector = connector
		self._sessionID = initStructure["sessionID"]

		self._ssh = initStructure["ssh"]
		self._ssh_dirPathData = initStructure.get("ssh_dirPathData")
		self._ssh_dirPathExtra = initStructure.get("ssh_dirPathExtra")
		self._ssh_dirPathRoot = initStructure.get("ssh_dirPathRoot")
		self._ssh_hostAddress = initStructure.get("ssh_hostAddress")
		self._ssh_login = initStructure.get("ssh_login")
		self._ssh_password = initStructure.get("ssh_password")
		self._ssh_port = initStructure.get("ssh_port")
		self._ssh_relPathData = initStructure.get("ssh_relPathData")
		self._ssh_relPathExtra = initStructure.get("ssh_relPathExtra")

		self.__mountPoint = None
	#

	@property
	def isReady(self) -> bool:
		return bool(self.__mountPoint)
	#

	@property
	def targetDirPath(self) -> str:
		if self.__mountPoint:
			return os.path.join(self.__mountPoint, self._ssh_relPathData)
		else:
			return None
	#

	@property
	def mountPoint(self) -> str:
		return self.__mountPoint
	#

	def initialize(self, backupDir:str):
		self.__backupDir = backupDir
	#

	def mountSSH(self, dirPath:str):
		assert isinstance(dirPath, str)
		assert os.path.isdir(dirPath)
		dirPath = os.path.abspath(dirPath)

		mounter = jk_mounting.Mounter()
		mip = mounter.getMountInfoByMountPoint(self._ssh_dirPathRoot)
		if mip is not None:
			raise Exception("Directory " + repr(self._ssh_dirPathRoot) + " already used by mount!")

		cmd = [
			BackupClient_ThaniyaSSH.SSHFS_PATH,
			"-p", str(self._ssh_port), "-o", "password_stdin", "-o", "reconnect", self._ssh_login + "@" + self._ssh_hostAddress + ":" + self._ssh_dirPathRoot, dirPath
		]

		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		p.stdin.write((self._ssh_password + "\n").encode("utf-8"))
		(stdout, stderr) = p.communicate(timeout=3)
		if p.returncode != 0:
			returnCode1 = p.returncode
			stdOutData1 = stdout.decode("utf-8")
			stdErrData1 = stderr.decode("utf-8")
			p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			p.stdin.write(("yes\n" + self._ssh_password + "\n").encode("utf-8"))
			(stdout, stderr) = p.communicate(timeout=3)
			if p.returncode != 0:
				returnCode2 = p.returncode
				stdOutData2 = stdout.decode("utf-8")
				stdErrData2 = stderr.decode("utf-8")
				print("Mount attempt 1:")
				print("\treturnCode =", returnCode1)
				print("\tstdOutData =", repr(stdOutData1))
				print("\tstdErrData =", repr(stdErrData1))
				print("Mount attempt 2:")
				print("\treturnCode =", returnCode2)
				print("\tstdOutData =", repr(stdOutData2))
				print("\tstdErrData =", repr(stdErrData2))
				raise Exception("Failed to mount device!")

		self.__mountPoint = dirPath
	#

	def umount(self, throwExceptionOnError:bool = True):
		assert isinstance(throwExceptionOnError, bool)

		if self.__mountPoint:
			cmd = [
				BackupClient_ThaniyaSSH.SUDO_PATH,
				BackupClient_ThaniyaSSH.UMOUNT_PATH,
				self.__mountPoint,
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
			else:
				self.__mountPoint = None
	#

	def __del__(self):
		self.umount(throwExceptionOnError=False)
	#

	def onBackupCompleted(self, bError:bool):
		self.umount(throwExceptionOnError=True)
	#

	def dump(self):
		print("BackupClient_ThaniyaSSH")
		for key in [ "_sessionID",
			"_ssh", "_ssh_dirPathData", "_ssh_dirPathExtra", "_ssh_dirPathRoot", "_ssh_hostAddress", "_ssh_login", "_ssh_password",
			"_ssh_port", "_ssh_relPathData", "_ssh_relPathExtra",
			"mountPoint" ]:
			print("\t" + key, "=", getattr(self, key))
	#

#













