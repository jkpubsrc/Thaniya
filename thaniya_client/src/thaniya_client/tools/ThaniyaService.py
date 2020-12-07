

import os
import typing
import tarfile

import jk_pathpatternmatcher2

from ..utils.ServiceInfo import ServiceInfo
from ..utils.ServiceMgr import ServiceMgr

from ..ThaniyaBackupContext import ThaniyaBackupContext





class ThaniyaService:

	@staticmethod
	def getServiceStatus(ctx:ThaniyaBackupContext, serviceName:str) -> ServiceInfo:
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(serviceName, str)
		assert serviceName

		ctx = ctx.descend("Retrieving state of service " + repr(serviceName) + " ...")
		with ctx.log as nestedLog:
			ret = ServiceMgr.getStatus(serviceName)

			nestedLog.notice("PID: " + str(ret.pid))
			nestedLog.notice("State: " + ret.sState)

			return ret
	#

	@staticmethod
	def serviceStart(ctx:ThaniyaBackupContext, serviceName:str):
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(serviceName, str)
		assert serviceName

		ctx = ctx.descend("Starting service " + repr(serviceName) + " ...")
		with ctx.log as nestedLog:
			ServiceMgr.start(serviceName)

			nestedLog.notice("Service started.")
	#

	@staticmethod
	def serviceStop(ctx:ThaniyaBackupContext, serviceName:str):
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(serviceName, str)
		assert serviceName

		ctx = ctx.descend("Stopping service: " + repr(serviceName) + " ...")
		with ctx.log as nestedLog:
			ServiceMgr.stop(serviceName)

			nestedLog.notice("Service stopped.")
	#

	@staticmethod
	def serviceRestore(ctx:ThaniyaBackupContext, serviceInfo:ServiceInfo):
		assert isinstance(ctx, ThaniyaBackupContext)
		assert isinstance(serviceInfo, ServiceInfo)

		ctx = ctx.descend("Restoring service " + repr(serviceInfo.serviceName) + " to previous state " + repr(serviceInfo.sState) + "...")
		with ctx.log as nestedLog:
			currentState = ServiceMgr.getStatus(serviceInfo.serviceName)
			nestedLog.notice("Current state: " + currentState.sState)
			nestedLog.notice("Target state: " + serviceInfo.sState)

			if serviceInfo.isRunning:
				if currentState.isRunning:
					nestedLog.notice("Nothing to do.")
				else:
					nestedLog.notice("Starting service ...")
					ServiceMgr.start(serviceInfo.serviceName)
					nestedLog.notice("Service started.")
			else:
				if currentState.isRunning:
					nestedLog.notice("Stopping service ...")
					ServiceMgr.stop(serviceInfo.serviceName)
					nestedLog.notice("Service stopped.")
				else:
					nestedLog.notice("Nothing to do.")
	#

#




































