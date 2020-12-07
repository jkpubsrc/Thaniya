

import os
import typing
import shutil
import time

import jk_utils
from jk_typing import checkFunctionSignature

from .utils.ServiceInfo import ServiceInfo
from .utils.ServiceMgr import ServiceMgr
from .ThaniyaBackupContext import ThaniyaBackupContext





class ThaniyaIO:

	class _Progress(object):

		def __init__(self, maxv:int):
			assert maxv > 0
			self.__maxv = maxv
			self.__t = 0
		#

		def printProgress(self, value:int):
			t = time.time()
			dt = t - self.__t
			if dt > 1:
				self.__t = t
			else:
				return

			f = value / self.__maxv
			if f < 0:
				f = 0
			if f > 1:
				f = 1
			f = f*100
			r = int(round(f))
			if r > 100:
				r = 100

			bar = "|" + "#" * r + "." * (100 - r) + "| " + str(round(f, 2)) + "% \r"
			print(bar, end="")
		#

		def clearProgress(self):
			print(" " * 110 + "\r", end="")
		#

	#

	#
	# Ensure that the specified directory exists. If it does not exist this method will create it.
	# If you specify a directory mode the directory access mask will be modified.
	#
	@staticmethod
	def ensureDirExists(ctx:ThaniyaBackupContext, dirPath:str, dirMode:typing.Union[int,str,jk_utils.ChModValue] = None):
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(dirPath, str)
		assert dirPath
		assert os.path.isabs(dirPath)
		if dirMode is not None:
			if isinstance(dirMode, int):
				dirMode = jk_utils.ChModValue(dirMode)
			elif isinstance(dirMode, str):
				dirMode = jk_utils.ChModValue(dirMode)
			elif isinstance(dirMode, jk_utils.ChModValue):
				pass
			else:
				raise Exception("dirMode is invalid!")

		with ctx.descend("Ensuring directory exists: " + repr(dirPath)) as ctx:
			if not os.path.isdir(dirPath):
				os.makedirs(dirPath)

			if dirMode is not None:
				ctx.log.notice("Setting directory mode: " + dirMode.toStr())
				os.chmod(dirPath, dirMode.toInt())
	#

	#
	# The directory access mask will be modified.
	#
	@staticmethod
	def ensureDirMode(ctx:ThaniyaBackupContext, dirPath:str, dirMode:typing.Union[int,str,jk_utils.ChModValue]):
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(dirPath, str)
		assert dirPath
		assert os.path.isabs(dirPath)

		if isinstance(dirMode, int):
			dirMode = jk_utils.ChModValue(dirMode)
		elif isinstance(dirMode, str):
			dirMode = jk_utils.ChModValue(dirMode)
		elif isinstance(dirMode, jk_utils.ChModValue):
			pass
		else:
			raise Exception("dirMode is invalid!")

		with ctx.descend("Ensuring mode for directory: " + repr(dirPath)) as ctx:
			if not os.path.isdir(dirPath):
				raise Exception("No such directory: " + dirPath)

			ctx.log.notice("Setting directory mode: " + dirMode.toStr())
			os.chmod(dirPath, dirMode.toInt())
	#

	#
	# Raise an exception if the specified directory does not exist.
	#
	@staticmethod
	def checkThatDirExists(ctx:ThaniyaBackupContext, dirPath:str):
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(dirPath, str)
		assert dirPath
		assert os.path.isabs(dirPath)

		with ctx.descend("Checking if directory exists: " + repr(dirPath)) as ctx:
			if os.path.isdir(dirPath):
				ctx.log.notice("Directory exists: " + dirPath)
			else:
				raise Exception("Directory does not exist: " + dirPath)
	#

	#
	# Raise an exception if the specified directory does not exist or is not empty.
	#
	@staticmethod
	def checkThatDirExistsAndIsEmpty(ctx:ThaniyaBackupContext, dirPath:str):
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(dirPath, str)
		assert dirPath
		assert os.path.isabs(dirPath)

		with ctx.descend("Checking if directory exists and is empty: " + repr(dirPath)) as ctx:
			if os.path.isdir(dirPath):
				ctx.log.notice("Directory exists: " + dirPath)
				contents = list(os.scandir(dirPath))
				if contents:
					raise Exception("Directory is not empty: " + dirPath)
				else:
					ctx.log.notice("Directory is empty: " + dirPath)
			else:
				raise Exception("Directory does not exist: " + dirPath)
	#

	#
	# Raise an exception if the specified directory does not exist. Scan the directory for files and subdirectories.
	# Return <c>True</c> or <c>False</c> if the directory is empty, together with a list of all directory entries.
	#
	@staticmethod
	def checkIfDirIsEmpty(ctx:ThaniyaBackupContext, dirPath:str) -> typing.Tuple[bool,typing.List[str]]:
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(dirPath, str)
		assert dirPath
		assert os.path.isabs(dirPath)

		with ctx.descend("Checking if directory is empty: " + repr(dirPath)) as ctx:
			if os.path.isdir(dirPath):
				contents = list(os.scandir(dirPath))
				if contents:
					ctx.log.notice("Directory " + repr(dirPath) + " contains entries!")
					return False, [ c.name for c in contents ]
				else:
					ctx.log.notice("Directory is empty: " + dirPath)
					return True, []
			else:
				raise Exception("Directory does not exist: " + dirPath)
	#

	#
	# Clean the specified directory. Cleaning means that everything within this directory - regardless of files, links or subdirectories - will
	# be deleted recursively.
	#
	@staticmethod
	def cleanDir(ctx:ThaniyaBackupContext, dirPath:str):
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(dirPath, str)
		assert os.path.isabs(dirPath)
		assert os.path.isdir(dirPath)

		with ctx.descend("Cleaning directory: " + repr(dirPath)) as ctx:
			for e in os.scandir(dirPath):
				if e.is_dir():
					shutil.rmtree(e.path)
				else:
					os.unlink(e.path)
	#

	@staticmethod
	def removeEmptyDir(ctx:ThaniyaBackupContext, dirPath:str):
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(dirPath, str)
		assert os.path.isabs(dirPath)
		assert os.path.isdir(dirPath)

		with ctx.descend("Removing empty directory: " + repr(dirPath)) as ctx:
			bIsEmpty, _ = ThaniyaIO.checkIfDirIsEmpty(ctx, dirPath)
			if bIsEmpty:
				ctx.log.notice("Removing directory: " + repr(dirPath))
				os.rmdir(dirPath)
			else:
				raise Exception("Directory not empty: " + dirPath)
	#

	#
	# Calculate the size of a directory tree.
	#
	@staticmethod
	def getDirTreeSize(ctx:ThaniyaBackupContext, dirPath:str) -> int:
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(dirPath, str)
		assert dirPath
		assert os.path.isabs(dirPath)
		assert os.path.isdir(dirPath)

		with ctx.descend("Calculating size of directory: " + repr(dirPath)) as ctx:
			n = jk_utils.fsutils.getFolderSize(dirPath)
			ctx.log.notice("Size of " + repr(dirPath) + ": " + jk_utils.formatBytes(n))
			return n
	#

	#
	# Get the size of a file.
	#
	@staticmethod
	def getFileSize(ctx:ThaniyaBackupContext, filePath:str) -> int:
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(filePath, str)
		assert filePath
		assert os.path.isabs(filePath)
		assert os.path.isfile(filePath)

		with ctx.descend("Getting size of file: " + repr(filePath)) as ctx:
			n = os.path.getsize(filePath)
			ctx.log.notice("Size of " + repr(filePath) + ": " + jk_utils.formatBytes(n))
			return n
	#

	#
	# Copy a file to another destination.
	#
	@staticmethod
	@checkFunctionSignature()
	def copyFile(ctx:ThaniyaBackupContext, sourceFilePath:str, targetFileOrDirectoryPath:str):
		assert sourceFilePath
		assert os.path.isabs(sourceFilePath)
		assert os.path.isfile(sourceFilePath)

		assert targetFileOrDirectoryPath
		targetFileOrDirectoryPath = ctx.absPath(targetFileOrDirectoryPath)

		# ----

		if os.path.isdir(targetFileOrDirectoryPath):
			#with ctx.descend("Copying file " + repr(sourceFilePath) + " to directory " + targetFileOrDirectoryPath + " ...") as ctx:
			#targetFilePath = os.path.join(targetFileOrDirectoryPath, os.path.basename(sourceFilePath))
			raise Exception("File names can not be generated automatically! You must specify a file as target!")

		with ctx.descend("Copying file " + repr(sourceFilePath) + " to file " + targetFileOrDirectoryPath + " ...") as ctx:
			targetFilePath = targetFileOrDirectoryPath

			nBytesToCopy = os.path.getsize(sourceFilePath)
			ctx.log.notice(str(nBytesToCopy) + " byte(s) to copy.")

			p = ThaniyaIO._Progress(nBytesToCopy)
			nBytesWritten = 0
			with open(sourceFilePath, "rb") as fin:
				with open(targetFilePath, "wb") as fout:
					while True:
						data = fin.read(65536 * 4)
						if not data:
							break
						fout.write(data)
						nBytesWritten += len(data)
						p.printProgress(nBytesWritten)

			p.clearProgress()
			ctx.log.notice("Success.")

			return nBytesToCopy
	#

	#
	# Get the size of a device in the <c>/dev/</c> directory.
	#
	@staticmethod
	@checkFunctionSignature()
	def getSizeOfDevice(ctx:ThaniyaBackupContext, devicePath:str) -> typing.Union[int,None]:
		assert devicePath.startswith("/dev/")

		with ctx.log as nestedLog:
			try:
				fd = os.open(devicePath, os.O_RDONLY)
				try:
					n = os.lseek(fd, 0, os.SEEK_END)
					nestedLog.notice("Size: " + jk_utils.formatBytes(n))
					return n
				finally:
					os.close(fd)
			except:
				raise Exception("Failed to access device: " + devicePath)
	#

	#
	# Copy all blocks from the specified device.
	#
	@staticmethod
	@checkFunctionSignature()
	def copyDevice(ctx:ThaniyaBackupContext, sourceDevicePath:str, targetFileOrDirectoryPath:str):
		assert sourceDevicePath
		assert sourceDevicePath.startswith("/dev/")
		assert os.path.isabs(sourceDevicePath)
		assert os.path.exists(sourceDevicePath)

		assert targetFileOrDirectoryPath
		targetFileOrDirectoryPath = ctx.absPath(targetFileOrDirectoryPath)

		# ----

		if os.path.isdir(targetFileOrDirectoryPath):
			#with ctx.descend("Copying data of device " + repr(sourceDevicePath) + " to directory " + targetFileOrDirectoryPath + " ...") as ctx:
			#targetFilePath = os.path.join(targetFileOrDirectoryPath, os.path.basename(sourceDevicePath))
			raise Exception("File names can not be generated automatically! You must specify a file as target!")

		with ctx.descend("Copying data of file " + repr(sourceDevicePath) + " to file " + targetFileOrDirectoryPath + " ...") as ctx:
			targetFilePath = targetFileOrDirectoryPath

			nBytesToCopy = ThaniyaIO.getSizeOfDevice(ctx, sourceDevicePath)
			ctx.log.notice(str(nBytesToCopy) + " byte(s) to copy.")

			p = ThaniyaIO._Progress(nBytesToCopy)
			nBytesWritten = 0
			with open(sourceDevicePath, "rb") as fin:
				with open(targetFilePath, "wb") as fout:
					while True:
						data = fin.read(65536 * 4)
						if not data:
							break
						fout.write(data)
						nBytesWritten += len(data)
						p.printProgress(nBytesWritten)

			p.clearProgress()
			ctx.log.notice("Success.")

			return nBytesToCopy
	#

#




































