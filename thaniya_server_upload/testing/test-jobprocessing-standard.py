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

	def processJob(self, ctx:JobProcessingCtx, job:Job):
		print("BEGIN noop")
		for i in range(0, 5):
			ctx.checkForTermination()
			time.sleep(1)
		print("END noop")
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
		if job.state not in [ EnumJobState.READY, EnumJobState.PROCESSING ]:
			break

	jobProcessingEngine.terminate()

	print()
	print()
	print()

	print("=" * 120)
	jobQueue.dump()
	print("=" * 120)















