

import os
import json
import typing

import jk_simpleexec
import jk_utils

from ..ThaniyaBackupContext import ThaniyaBackupContext

from .EnumTarPathMode import EnumTarPathMode
from .ThaniyaService import ThaniyaService






class ThaniyaMySQL:

	assert os.path.dirname(__file__).startswith("/usr/local/")
	__GET_DB_SIZE_HELPER_PATH = "/usr/local/bin/thania_helper_mysql_get_db_size.py"

	@staticmethod
	def mySQLDump(ctx:ThaniyaBackupContext, dbName:str, dbUserName:str, dbPassword:str, outputDumpFilePath:str):

		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(dbName, str)
		assert dbName
		assert isinstance(outputDumpFilePath, str)
		assert outputDumpFilePath

		ctx = ctx.descend("Creating dump file " + repr(outputDumpFilePath) + " ...")
		with ctx.log as nestedLog:
			outputDumpFilePath = ctx.absPath(outputDumpFilePath)

			authFile = ctx.privateTempDir.writeTextFile("[mysqldump]\nuser=" + dbUserName + "\npassword=" + dbPassword + "\n")
			result = jk_simpleexec.invokeCmd("/usr/bin/mysqldump", [
				"--defaults-extra-file=" + authFile,
				"-r",
				outputDumpFilePath,
				"--routines",				# Include stored routines (procedures and functions) for the dumped databases in the output.
				"--triggers",				# Include triggers for each dumped table in the output.
				dbName,
			], workingDirectory=os.path.dirname(authFile))

			if result.returnCode == 0:
				nestedLog.notice("Succeeded.")
				return os.path.getsize(outputDumpFilePath)
			else:
				result.dump(writeFunction=nestedLog.error)
				raise Exception("Failed to backup database '" + dbName + "'!")
	#

	@staticmethod
	def mySQLDumpCalculateSize(ctx:ThaniyaBackupContext, dbName:str, dbUserName:str, dbPassword:str) -> int:

		assert isinstance(ctx, ThaniyaBackupContext)

		ctx = ctx.descend("Calculating size for the MySQL dump ...")
		with ctx.log as nestedLog:

			nestedLog.notice("Invoking helper script ...")

			result = jk_simpleexec.invokeCmd(
				ThaniyaMySQL.__GET_DB_SIZE_HELPER_PATH,
				[],
				dataToPipeAsStdIn = json.dumps({
					"dbName": dbName,
					"dbUserName": dbUserName,
					"dbPassword": dbPassword,
					"dbPort": 3306,
				})
			)
			if result.returnCode != 0:
				result.dump(writeFunction=nestedLog.error)
				raise Exception("Failed to get dermine of database!")

			n = int(result.stdOutLines[0])
			nestedLog.notice("Database size: " + str(n))
			return n
	#

#


























