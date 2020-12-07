
import os
import signal
import subprocess

import jk_pathpatternmatcher2
import jk_utils
import jk_json
import jk_mediawiki
from jk_typing import checkFunctionSignature

from ..ThaniyaBackupContext import ThaniyaBackupContext
from ..tools.EnumTarPathMode import EnumTarPathMode
from ..tools.ThaniyaTar import ThaniyaTar

from .AbstractThaniyaTask import AbstractThaniyaTask





#
# This backup task addresses local MediaWiki installations.
#
class TBackupMediaWiki_User(AbstractThaniyaTask):

	_FULL_BACKUP = False		# if True all directories are considered for backup, even caching directories.

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Configuration parameters:
	#
	# @param	str mediaWikiDirPath		(required) The absolute directory path where the MediaWiki installation can be found.
	#										The final directory name in the path must be the same as the site name of the Wiki.
	#										Additionally there must be a cron script named "<sitename>cron.sh".
	# @param	str userName				(required) The name of the user account under which NGINX, PHP and the Wiki cron process are executed.
	#
	@checkFunctionSignature()
	def __init__(self,
		mediaWikiDirPath:str,
		userName:str,
		):

		self.__mwHelper = jk_mediawiki.MediaWikiLocalUserInstallationMgr(mediaWikiDirPath, userName)

		if not TBackupMediaWiki_User._FULL_BACKUP:
			self.__ignoreDirPathPatterns = [
				os.path.join(self.__mwHelper.wikiDirPath, "BAK"),
				os.path.join(self.__mwHelper.wikiDirPath, "cache"),
				os.path.join(self.__mwHelper.wikiDirPath, "images", "thumb"),
				os.path.join(self.__mwHelper.wikiDirPath, "images", "graphviz"),
			]
		else:
			self.__ignoreDirPathPatterns = None
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def logMessageCalculateSpaceRequired(self) -> str:
		return "Calculating backup size of MediaWiki installation: " + repr(self.__mwHelper.wikiDirName)
	#

	@property
	def logMessagePerformBackup(self) -> str:
		return "Performing backup of MediaWiki installation: " + repr(self.__mwHelper.wikiDirName)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def calculateSpaceRequired(self, ctx:ThaniyaBackupContext) -> int:
		# process root directory

		nErrorsWikiRoot, nSizeWikiRoot = ThaniyaTar.tarCalculateSize(
			ctx,
			jk_pathpatternmatcher2.walk(
				self.__mwHelper.wikiDirPath,
				ignoreDirPathPatterns = self.__ignoreDirPathPatterns
			)
		)
		ctx.log.info("I/O expected: " + jk_utils.formatBytes(nSizeWikiRoot))

		# process database directory

		nErrorsDBRoot, nSizeDBRoot = ThaniyaTar.tarCalculateSize(
			ctx,
			jk_pathpatternmatcher2.walk(
				self.__mwHelper.wikiDBDirPath
			)
		)
		ctx.log.info("I/O expected: " + jk_utils.formatBytes(nSizeDBRoot))

		return nSizeWikiRoot + nSizeDBRoot
	#

	def performBackup(self, ctx:ThaniyaBackupContext):

		def errorCallback(entry:jk_pathpatternmatcher2.Entry, exception):
			ctx.log.warn(str(exception))
			#ctx.log.error(str(exception))
		#

		# shut down various processes

		bIsRunning = self.__mwHelper.isCronScriptRunning()
		if bIsRunning:
			self.__mwHelper.stopCronScript(ctx.log.descend("Stopping cron process(es) ..."))
		else:
			ctx.log.notice("No cron process(es) need to be stopped and later restarted as they are not running.")

		# process root directory

		ThaniyaTar.tar(
			ctx=ctx,
			outputTarFilePath=ctx.absPath(self.__mwHelper.wikiDirName + "-wiki.tar"),
			walker=jk_pathpatternmatcher2.walk(
				self.__mwHelper.wikiDirPath,
				ignoreDirPathPatterns = self.__ignoreDirPathPatterns
			),
			pathMode=EnumTarPathMode.RELATIVE_PATH_WITH_BASE_DIR,
			onErrorCallback=errorCallback,
		)

		# process database directory

		ThaniyaTar.tar(
			ctx=ctx,
			outputTarFilePath=ctx.absPath(self.__mwHelper.wikiDirName + "-sqlite.tar"),
			walker=jk_pathpatternmatcher2.walk(
				self.__mwHelper.wikiDBDirPath,
				ignoreDirPathPatterns = self.__ignoreDirPathPatterns
			),
			pathMode=EnumTarPathMode.RELATIVE_PATH_WITH_BASE_DIR,
			onErrorCallback=errorCallback,
		)

		# restart processes

		if bIsRunning:
			self.__mwHelper.startCronScript(ctx.log.descend("Restarting cron process(es) ..."))
	#

#









