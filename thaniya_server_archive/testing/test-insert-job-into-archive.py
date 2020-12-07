#!/usr/bin/python3



##
## This test:
##	* copies the data tree "data.sav" to "data" to have something to work with
##	* checks that the archive is empty
##	* reads an incoming backup and inserts it into the archive (with compressing)
##	* checks that the archive now contains a single backup
##





import os
import shutil

import jk_logging

from thaniya_common.utils import IOContext
from thaniya_server_archive import *






DATA_WORK_DIR_NAME = "data"
DATA_SOURCE_DIR_NAME = "data.sav"







with jk_logging.wrapMain() as log:

	ioContext = IOContext()

	if os.path.isdir(DATA_WORK_DIR_NAME):
		shutil.rmtree(DATA_WORK_DIR_NAME)
	shutil.copytree(DATA_SOURCE_DIR_NAME, DATA_WORK_DIR_NAME)

	processingRuleSet = ProcessingRuleSet([
		ProcessingRule(FileNamePattern("*.tar"), "gzip"),
	])
	archive = ArchiveDataStore(ioContext, "data/archive/data", "data/archive/temp", bReadWrite=True, log=log)
	assert len(archive.backups) == 0

	jp = JobProcessor_InsertIntoArchive(ioContext, "data/uploaded", archive, processingRuleSet)

	job = Job("data/jobs/myjob.json")

	jp.process(job, log)

	assert len(archive.backups) == 1






