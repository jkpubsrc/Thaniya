#!/usr/bin/python3



from _testprg import *

from thaniya_server.jobs import JobQueueInlet
from thaniya_server.utils.ProcessFilter import ProcessFilter
from thaniya_server.utils.ProcessNotifier import ProcessNotifier







OUTPUT_DIR = "/srv/thaniya/archive-jobQueue"




with testPrg(__file__, hasTempDir=True) as (ioCtx, dataDirPath, tempDirPath, log):

	jobQueueInlet = JobQueueInlet(
		ioContext=ioCtx,
		dirPath=OUTPUT_DIR,
		log=log
	)

	log.info("Scheduling job")
	jobQueueInlet.scheduleJob("Noop", 10, {
		"myData": "noop"
	})

	processFilter_thaniyaArchiveHttpd = ProcessFilter(cmdMatcher= lambda x: x.find("python") > 0, argsMatcher= lambda x: x and (x.find("thaniya-archive-httpd.py") >= 0))
	processNotifier = ProcessNotifier(processFilter_thaniyaArchiveHttpd)
	n = processNotifier.notifySIGUSR1()
	log.info("{} Thaniya process(es) notified.".format(n))




































