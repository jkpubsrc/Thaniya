#!/usr/bin/python3



import typing
import os
import sys

import shutil

import jk_json
import jk_utils
import jk_logging

from thaniya_common.utils import IOContext

from thaniya_server.jobs import *













with jk_logging.wrapMain() as log:

	ioCtx = IOContext()

	dirPath = os.path.abspath("_" + os.path.splitext(os.path.basename(__file__))[0] + ".dir")
	if os.path.isdir(dirPath):
		shutil.rmtree(dirPath)
	ioCtx.ensureDirExists(dirPath)

	# ----

	jobQueue = JobQueue(ioCtx, dirPath, True, log)
	jobQueue.scheduleJob("foo", 0, { "foo": "bar" })
	jobQueue.dump()

	print()

	jobQueue = JobQueue(ioCtx, dirPath, True, log)
	jobQueue.dump()
	assert len(jobQueue.jobs) == 1

	print()

	job = jobQueue.getNextWaitingJob()
	job.state = EnumJobState.PROCESSING
	jobQueue.dump()
	job.storeProcessingState()

	print()

	jobQueue = JobQueue(ioCtx, dirPath, False, log)
	jobQueue.dump()
	assert len(jobQueue.jobs) == 1
	job = jobQueue.getNextWaitingJob()
	assert job is None

	print()

	jobQueue = JobQueue(ioCtx, dirPath, True, log)
	jobQueue.dump()
	assert len(jobQueue.jobs) == 1
	job = jobQueue.getNextWaitingJob()
	assert job is not None

















