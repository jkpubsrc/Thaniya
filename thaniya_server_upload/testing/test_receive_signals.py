#!/usr/bin/python3



import time
import os
import signal

import jk_json

from thaniya_server.utils import *



def handler(signum, frame):
	signals = {
		signal.SIGHUP: "SIGHUP",
		signal.SIGUSR1: "SIGUSR1",
		signal.SIGUSR2: "SIGUSR2",
	}
	print(signals[signum])
#


signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGUSR2, handler)


while True:
	time.sleep(1000)



