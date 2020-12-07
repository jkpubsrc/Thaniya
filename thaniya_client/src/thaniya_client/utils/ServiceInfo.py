#
# For this module to work you require either to invoke this as root or add the following line to your sudoers file (assuming you
# invoke the script being "myuser"):
#
# <code>
# myuser         ALL=(root) NOPASSWD: /usr/sbin/service
# </code>
#


import os
import typing






class ServiceInfo:

	def __init__(self, serviceName:str, description:str, active:str, isRunning:bool, pid:int):
		self.__serviceName = serviceName
		self.__description = description
		self.__active = active
		self.__isRunning = isRunning
		self.__pid = pid
	#

	@property
	def pid(self) -> int:
		return self.__pid
	#

	@property
	def isRunning(self) -> bool:
		return self.__isRunning
	#

	@property
	def description(self) -> str:
		return self.__description
	#

	@property
	def serviceName(self) -> str:
		return self.__serviceName
	#

	@property
	def sState(self):
		if self.__isRunning:
			return "running"
		else:
			return "stopped"
	#

	def __str__(self):
		return "<Service(" + repr(self.__serviceName) + ", " + self.sState + ", " + repr(self.description) + ")>"
	#

	def __repr__(self):
		return "<Service(" + repr(self.__serviceName) + ", " + self.sState + ", " + repr(self.description) + ")>"
	#

#














