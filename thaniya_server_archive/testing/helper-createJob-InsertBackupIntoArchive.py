#!/usr/bin/python3



from _testprg import *

from thaniya_server.jobs import JobQueueInlet
from thaniya_server.utils.ProcessFilter import ProcessFilter
from thaniya_server.utils.ProcessNotifier import ProcessNotifier







OUTPUT_DIR = "/srv/thaniya/archive-jobQueue"




with testPrg(__file__, hasTempDir=True) as (ioCtx, dataDirPath, tempDirPath, log):

	# create some files

	with open(os.path.join(tempDirPath, "foobar.txt"), "w") as f:
		f.write("Foo Bar\n")
	with open(os.path.join(tempDirPath, "lorem-ipsum.txt"), "w") as f:
		f.write("Lorem Ipsum\n")

	# create a processing job

	jobQueueInlet = JobQueueInlet(
		ioContext=ioCtx,
		dirPath=OUTPUT_DIR,
		log=log
	)

	log.info("Scheduling job")
	jobQueueInlet.scheduleJob("InsertBackupIntoArchive", 10, {
		"dirPath": tempDirPath,
		"dataFileNames": [
			"foobar.txt",
			"lorem-ipsum.txt"
		],
		"metaFileNames": [
		],
		"tBackupStart": 1608290014.423183,
		"tBackupEnd": 1608286417.623469,
		"dClientBackupDuration": 1.199193716,
		"sizeInBytes": 12378112,
		"systemName": "selenium",
		"backupUserName": "woodoo",
		"backupIdentifier": "fooBar",
	})

	# signal the application that a new job arrived

	processFilter_thaniyaArchiveHttpd = ProcessFilter(cmdMatcher= lambda x: x.find("python") > 0, argsMatcher= lambda x: x and (x.find("thaniya-archive-httpd.py") >= 0))
	processNotifier = ProcessNotifier(processFilter_thaniyaArchiveHttpd)
	n = processNotifier.notifySIGUSR1()
	log.info("{} Thaniya process(es) notified.".format(n))




































