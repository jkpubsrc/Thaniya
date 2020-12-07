


import typing
import os
import json
import hashlib
import shutil

import jk_utils







class IOContext(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		self.__chmodValueDir = jk_utils.ChModValue("rwx------")
		self.__chmodValueDirI = self.__chmodValueDir.toInt()

		self.__chmodValueFile = jk_utils.ChModValue("rw-------")
		self.__chmodValueFileI = self.__chmodValueFile.toInt()

		self.__spoolChunkSize = 262144	 	# 256K
		self.__bAutoFlush = False
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def chmodValueDir(self) -> jk_utils.ChModValue:
		return self.__chmodValueDir
	#

	@property
	def chmodValueDirI(self) -> int:
		return self.__chmodValueDirI
	#

	@property
	def chmodValueFile(self) -> jk_utils.ChModValue:
		return self.__chmodValueFile
	#

	@property
	def chmodValueFileI(self) -> int:
		return self.__chmodValueFileI
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def absPath(self, baseDirPath:str, path:str):
		if os.path.isabs(path):
			return path
		else:
			return os.path.join(baseDirPath, path)
	#

	def makeDir(self, dirPath:str):
		os.makedirs(dirPath, self.__chmodValueDirI)
		os.chmod(dirPath, self.__chmodValueDirI)
	#

	def setDirMode(self, dirPath:str):
		os.chmod(dirPath, self.__chmodValueDirI)
	#

	def setFileMode(self, filePath:str):
		os.chmod(filePath, self.__chmodValueFileI)
	#

	def writeToFileStr(self, strData:str, filePath:str, bFlush:bool = False, bSafe:bool = False):
		if bSafe:

			tmpFilePath = filePath + ".tmp"
			bakFilePath = filePath + ".bak"

			fdesc = os.open(tmpFilePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.__chmodValueFileI)
			with os.fdopen(fdesc, "w") as f:
				f.write(strData)
				if self.__bAutoFlush or bFlush:
					f.flush()

			if os.path.isfile(bakFilePath):
				os.unlink(bakFilePath)

			if os.path.isfile(filePath):
				os.rename(filePath, bakFilePath)
			os.rename(tmpFilePath, filePath)
			if os.path.isfile(bakFilePath):
				os.unlink(bakFilePath)

		else:

			fdesc = os.open(filePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.__chmodValueFileI)
			with os.fdopen(fdesc, "w") as f:
				f.write(strData)
				if self.__bAutoFlush or bFlush:
					f.flush()
	#

	def writeToFileJSON(self, jsonData, filePath:str, bPretty:bool, bFlush:bool = False, bSafe:bool = False):
		assert isinstance(jsonData, (str,float,int,bool,list,dict))
		if bPretty:
			strData = json.dumps(jsonData, indent="\t")
		else:
			strData = json.dumps(jsonData, separators=(",", ":"))
		self.writeToFileStr(strData, filePath, bFlush, bSafe)
	#

	def writeToFileBinary(self, binData:typing.Union[bytes,bytearray], filePath:str, bFlush:bool = False, bSafe:bool = False):
		if bSafe:

			tmpFilePath = filePath + ".tmp"
			bakFilePath = filePath + ".bak"

			fdesc = os.open(tmpFilePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.__chmodValueFileI)
			with os.fdopen(fdesc, "wb") as f:
				f.write(binData)
				if self.__bAutoFlush or bFlush:
					f.flush()

			if os.path.isfile(bakFilePath):
				os.unlink(bakFilePath)

			if os.path.isfile(filePath):
				os.rename(filePath, bakFilePath)
			os.rename(tmpFilePath, filePath)
			if os.path.isfile(bakFilePath):
				os.unlink(bakFilePath)

		else:

			fdesc = os.open(filePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.__chmodValueFileI)
			with os.fdopen(fdesc, "wb") as f:
				f.write(binData)
				if self.__bAutoFlush or bFlush:
					f.flush()
	#

	def openWriteBinary(self, filePath:str):
		fdesc = os.open(filePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.__chmodValueFileI)
		return os.fdopen(fdesc, "wb")
	#

	def openWriteText(self, filePath:str):
		fdesc = os.open(filePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.__chmodValueFileI)
		return os.fdopen(fdesc, "w")
	#

	def tryReadFromFileBinary(self, filePath:str, bSafe:bool = False) -> bytes:
		if bSafe:

			if os.path.isfile(filePath):
				with open(filePath, "rb") as f:
					return f.read()
			else:
				bakFilePath = filePath + ".bak"
				if os.path.isfile(bakFilePath):
					with open(filePath, "rb") as f:
						return f.read()

		else:

			if os.path.isfile(filePath):
				with open(filePath, "rb") as f:
					return f.read()

		return None
	#

	def tryReadFromFileJSON(self, filePath:str, bSafe:bool = False):
		s = self.tryReadFromFileStr(filePath, bSafe)
		if s is None:
			return None
		return json.loads(s)
	#

	def tryReadFromFileStr(self, filePath:str, bSafe:bool = False) -> str:
		if bSafe:

			if os.path.isfile(filePath):
				with open(filePath, "r") as f:
					return f.read()
			else:
				bakFilePath = filePath + ".bak"
				if os.path.isfile(bakFilePath):
					with open(filePath, "r") as f:
						return f.read()

		else:

			if os.path.isfile(filePath):
				with open(filePath, "r") as f:
					return f.read()

		return None
	#

	def readFromFileBinary(self, filePath:str, bSafe:bool = False) -> bytes:
		if bSafe:

			if os.path.isfile(filePath):
				with open(filePath, "rb") as f:
					return f.read()
			else:
				bakFilePath = filePath + ".bak"
				if os.path.isfile(bakFilePath):
					with open(filePath, "rb") as f:
						return f.read()

		else:

			if os.path.isfile(filePath):
				with open(filePath, "rb") as f:
					return f.read()

		raise Exception("File not found: " + repr(filePath))
	#

	def readFromFileJSON(self, filePath:str, bSafe:bool = False):
		s = self.readFromFileStr(filePath, bSafe)
		return json.loads(s)
	#

	def readFromFileStr(self, filePath:str, bSafe:bool = False) -> str:
		if bSafe:

			if os.path.isfile(filePath):
				with open(filePath, "r") as f:
					return f.read()
			else:
				bakFilePath = filePath + ".bak"
				if os.path.isfile(bakFilePath):
					with open(filePath, "r") as f:
						return f.read()

		else:

			if os.path.isfile(filePath):
				with open(filePath, "r") as f:
					return f.read()

		raise Exception("File not found: " + repr(filePath))
	#

	#
	# @return		bool			Returns <c>False</c> if the directory did not exist and was created. <c>True</c> is returend if the directory already existed.
	#
	def ensureDirExists(self, dirPath:str) -> bool:
		if os.path.isdir(dirPath):
			os.chmod(dirPath, self.__chmodValueDirI)
			return True
		else:
			os.makedirs(dirPath, self.__chmodValueDirI, exist_ok=True)
			os.chmod(dirPath, self.__chmodValueDirI)
			return False
	#

	def cleanDir(self, dirPath:str):
		for fe in os.scandir(dirPath):
			if fe.is_dir():
				shutil.rmtree(fe.path, ignore_errors=False)
			else:
				os.unlink(fe.path)
	#

	#
	# Remove the specified directory (including all files and subdirectories recursively).
	# An exception is raised if deleting fails for some reason.
	#
	def removeDir(self, dirPath:str):
		shutil.rmtree(dirPath, ignore_errors=False)
	#

	#
	# Efficiently move a file from source to destination.
	#
	def moveFile(self, fromFilePath:str, toFilePath:str, bFlush:bool = False):
		fromDev = os.stat(fromFilePath).st_dev
		toDirPath = os.path.dirname(toFilePath)
		toDev = os.stat(toDirPath).st_dev

		nChunkSize = 262144	 	# 256K

		if fromDev == toDev:
			# files reside on the same volume
			os.rename(fromFilePath, toFilePath)
			os.chmod(toFilePath, self.__chmodValueFileI)

		else:
			# files do not reside on the same volume
			buffer = bytearray(nChunkSize)
			with open(fromFilePath, "rb") as fin:
				fdesc = os.open(toFilePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.__chmodValueFileI)
				with os.fdopen(fdesc, "wb") as fout:
					while True:
						buffer = fin.read(nChunkSize)
						if buffer:
							fout.write(buffer)
						else:
							break
					if self.__bAutoFlush or bFlush:
						fout.flush()
				os.close(fdesc)
			os.unlink(fromFilePath)
	#

	#
	# @return		int			Returns the number of bytes written.
	#
	def spoolStreams(self, fin, fout, bFlush:bool = False) -> int:
		nTotalSize = 0
		nChunkSize = self.__spoolChunkSize

		# files do not reside on the same volume
		buffer = bytearray(nChunkSize)
		while True:
			buffer = fin.read(nChunkSize)
			if buffer:
				nTotalSize += len(buffer)
				fout.write(buffer)
			else:
				break
		if self.__bAutoFlush or bFlush:
			fout.flush()
		return nTotalSize
	#

	def _createHashAlg(self, hashAlgName:str):
		if hashAlgName == "md5":
			return hashlib.md5()
		elif hashAlgName == "sha1":
			return hashlib.sha1()
		elif hashAlgName == "sha224":
			return hashlib.sha224()
		elif hashAlgName == "sha256":
			return hashlib.sha256()
		elif hashAlgName == "sha512":
			return hashlib.sha512()
		else:
			raise Exception("Unknown hash algorithm: " + repr(hashAlgName))
	#

	#
	# Calculate the hash sum of the specified file.
	#
	# @param		str filePath		The file to calculate the hash for.
	# @param		str hashAlgName		One of the supported hash algorithm names: "md5", "sha1", "sha224", "sha256", "sha512"
	# @return		str digest			Returns a string representation of the calculated hash value.
	#
	def fileCalcHash(self, filePath:str, hashAlgName:str) -> str:
		hashAlg = self._createHashAlg(hashAlgName)
		nChunkSize = self.__spoolChunkSize
		buffer = bytearray(nChunkSize)

		with open(filePath, "rb") as fin:
			while True:
				buffer = fin.read(nChunkSize)
				if buffer:
					hashAlg.update(buffer)
				else:
					break

		return hashAlg.hexdigest()
	#

	#
	# Move (or copy-delete) a file from source to destination and calculate it's hash value.
	#
	# @param		str filePath		The file to calculate the hash for.
	# @param		str hashAlgName		One of the supported hash algorithm names: "md5", "sha1", "sha224", "sha256", "sha512"
	# @return		str digest			Returns a string representation of the calculated hash value.
	#
	def moveFileCalcHash(self, fromFilePath:str, toFilePath:str, hashAlgName:str, bFlush:bool = False) -> str:
		fromDev = os.stat(fromFilePath).st_dev
		toDirPath = os.path.dirname(toFilePath)
		toDev = os.stat(toDirPath).st_dev

		hashAlg = self._createHashAlg(hashAlgName)
		nChunkSize = self.__spoolChunkSize

		if fromDev == toDev:
			# files reside on the same volume

			with open(fromFilePath, "rb") as f:
				for buffer in iter(lambda: f.read(nChunkSize), b""):
					hashAlg.update(buffer)

			os.rename(fromFilePath, toFilePath)
			os.chmod(toFilePath, self.__chmodValueFileI)

		else:
			# files do not reside on the same volume
			buffer = bytearray(nChunkSize)
			with open(fromFilePath, "rb") as fin:
				fdesc = os.open(toFilePath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, self.__chmodValueFileI)
				with os.fdopen(fdesc, "wb") as fout:
					while True:
						buffer = fin.read(nChunkSize)
						if buffer:
							hashAlg.update(buffer)
							fout.write(buffer)
						else:
							break
					if self.__bAutoFlush or bFlush:
						fout.flush()
				os.close(fdesc)
			os.unlink(fromFilePath)

		return hashAlg.hexdigest()
	#

#









