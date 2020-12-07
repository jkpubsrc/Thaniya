

import os
import typing
import signal

import jk_typing
import jk_json

from .ProcessFilter import ProcessFilter










class ProcessNotifier(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, *processFilters):
		for p in processFilters:
			assert isinstance(p, ProcessFilter)
		self.__processFilters = processFilters
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def notifySIGHUP(self) -> int:
		n = 0
		for processFilter in self.__processFilters:
			for jProc in processFilter.findProcessStructs():
				os.kill(jProc["pid"], signal.SIGHUP)
				n += 1
		return n
	#

	def notifySIGUSR1(self) -> int:
		n = 0
		for processFilter in self.__processFilters:
			for jProc in processFilter.findProcessStructs():
				os.kill(jProc["pid"], signal.SIGUSR1)
				n += 1
		return n
	#

	def notifySIGUSR2(self) -> int:
		n = 0
		for processFilter in self.__processFilters:
			for jProc in processFilter.findProcessStructs():
				os.kill(jProc["pid"], signal.SIGUSR2)
				n += 1
		return n
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#









