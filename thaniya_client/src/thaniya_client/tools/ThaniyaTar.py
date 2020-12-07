

import os
import typing
import tarfile

import jk_pathpatternmatcher2
import jk_utils

from ..ThaniyaBackupContext import ThaniyaBackupContext

from .EnumTarPathMode import EnumTarPathMode





class ThaniyaTar:

	@staticmethod
	def __createTarInfo(e, pathMode):
		if pathMode == EnumTarPathMode.RELATIVE_PATH:
			t = tarfile.TarInfo(e.relPath)
		elif pathMode == EnumTarPathMode.RELATIVE_PATH_WITH_BASE_DIR:
			if e.baseDirPath == "/":
				baseDirName = ""
			else:
				baseDirName = os.path.basename(e.baseDirPath)
				baseDirName += "/"
			t = tarfile.TarInfo(baseDirName + e.relPath)
		elif pathMode == EnumTarPathMode.FULL_PATH:
			t = tarfile.TarInfo(e.fullPath[1:])
		elif pathMode == EnumTarPathMode.ABSOLUTE_PATH:
			t = tarfile.TarInfo(e.fullPath)
		else:
			raise Exception("Invalid value specified for pathMode: " + repr(pathMode))

		t.uname = e.user
		t.gname = e.group
		t.mtime = e.mtime

		return t
	#

	@staticmethod
	def tar(ctx:ThaniyaBackupContext, outputTarFilePath:str, walker:typing.Sequence[jk_pathpatternmatcher2.Entry],
		onErrorCallback = None, pathMode:EnumTarPathMode = EnumTarPathMode.RELATIVE_PATH) -> typing.Tuple[int,int]:

		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(outputTarFilePath, str)
		if onErrorCallback:
			assert callable(onErrorCallback)
		assert isinstance(pathMode, EnumTarPathMode)

		ctx = ctx.descend("Creating tar file " + repr(outputTarFilePath) + " ...")
		with ctx.log as nestedLog:
			outputTarFilePath = ctx.absPath(outputTarFilePath)

			nErrors = 0
			nSize = 0

			with tarfile.open(outputTarFilePath, "w") as ftar:

				for e in walker:
					assert isinstance(e, jk_pathpatternmatcher2.Entry)

					if e.type == "f":
						nSize += e.size

						t = ThaniyaTar.__createTarInfo(e, pathMode)
						t.size = e.size
						try:
							with open(e.fullPath, "rb") as fin:
								ftar.addfile(t, fin)
						except Exception as ee:
							nErrors += 1
							if onErrorCallback:
								onErrorCallback(e, ee)

					elif e.type == "d":
						nSize += e.size

						t = ThaniyaTar.__createTarInfo(e, pathMode)
						t.type = tarfile.DIRTYPE
						ftar.addfile(t, None)

					elif e.type == "l":
						nSize += e.size

						t = ThaniyaTar.__createTarInfo(e, pathMode)
						t.type = tarfile.SYMTYPE
						t.linkname = e.linkText
						ftar.addfile(t, None)

					elif e.type.startswith("e"):
						nErrors += 1
						if onErrorCallback:
							onErrorCallback(e, e.exception)

			return nErrors, nSize
	#

	@staticmethod
	def tarCalculateSize(ctx:ThaniyaBackupContext, walker:typing.Sequence[jk_pathpatternmatcher2.Entry],
		onErrorCallback = None) -> typing.Tuple[int,int]:

		assert isinstance(ctx, ThaniyaBackupContext)
		if onErrorCallback:
			assert callable(onErrorCallback)

		ctx = ctx.descend("Calculating size for tar file ...")
		with ctx.log as nestedLog:

			nErrors = 0
			nSize = 0

			for e in walker:
				assert isinstance(e, jk_pathpatternmatcher2.Entry)

				if e.type == "f":
					nSize += e.size

				elif e.type == "d":
					nSize += e.size

				elif e.type == "l":
					nSize += e.size

				elif e.type.startswith("e"):
					nErrors += 1
					if onErrorCallback:
						onErrorCallback(e, e.exception)

			return nErrors, nSize
	#

#


























