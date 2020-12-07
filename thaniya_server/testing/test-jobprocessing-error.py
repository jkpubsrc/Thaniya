#!/usr/bin/python3



from _testprg import *

from thaniya_server.jobs import *

"""

This file allows testing the job queue and job processing. A job queue is generated, a job is inserted, and a job processer picks it up
and processes the job. But after three seconds job processing is interrupted, so that you will see a <c>InterruptedException</c> error message.

"""











class MyJobProcessor(AbstractJobProcessor):

	def __init__(self):
		super().__init__("noop")
	#

	def __secondSubRoutine(self, ctx:JobProcessingCtx, log:jk_logging.AbstractLogger):
		with log.descend("Doing something ...") as log2:
			ctx.checkForTermination()
			log2.notice("NOOP: sleeping for 1 second")
			time.sleep(1)
			log2.warn("NOOP: now failing intentionally ...")
			x = 0
			y = 3 / x
	#

	def __subRoutine(self, ctx:JobProcessingCtx, log:jk_logging.AbstractLogger):
		with log.descend("Doing something ...") as log2:
			self.__secondSubRoutine(ctx, log2)
	#

	def processJob(self, ctx:JobProcessingCtx, job:Job):
		with ctx.log.descend("No processing: NOOP") as log2:
			log2.notice("NOOP begin")
			self.__subRoutine(ctx, log2)
			log2.notice("NOOP end")
	#

#





with testPrg(__file__, hasTempDir=True) as (ioCtx, dataDirPath, tempDirPath, log):

	jobProcessingEngine = JobProcessingEngine(log, dirPath = tempDirPath)
	jobProcessingEngine.register(MyJobProcessor())

	jobQueue = JobQueue(
		ioContext=ioCtx,
		dirPath=tempDirPath,
		bResetJobStateOnLoad=True,
		log=log
	)
	jobProcessingEngine.start(jobQueue)
	
	job = jobQueue.scheduleJob("noop", 0, { "foo": "bar" })
	
	while True:
		time.sleep(1)
		print(job.state)
		if job.state in [ EnumJobState.INTERRUPTED, EnumJobState.ERROR, EnumJobState.SUCCESS, EnumJobState.SUSPENDED ]:
			break

	jobProcessingEngine.terminate()

	print()
	print()
	print()

	print("=" * 120)
	jobQueue.dump()
	print("=" * 120)














