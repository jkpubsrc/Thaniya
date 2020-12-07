



import os
import typing
import time

import jk_typing
import jk_utils
import jk_logging
import jk_json
import jk_prettyprintobj

from thaniya_server.jobs import Job
from thaniya_server.jobs import AbstractJobProcessor
from thaniya_server.jobs import JobProcessingCtx

from .archive import ArchivedBackupInfoFile
from .archive import ArchiveManager
from .archive import ArchiveDataStore
from .archive.ProcessingRule import ProcessingRule
from .archive.ProcessingRuleSet import ProcessingRuleSet







class JobProcessor_Noop(AbstractJobProcessor):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	@jk_typing.checkFunctionSignature()
	def __init__(self):
		super().__init__("Noop")
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################


	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def processJob(self, ctx:JobProcessingCtx, job:Job):
		ctx.log.notice("Doing nothing.")
	#

#























