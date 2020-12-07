# NOTE: This is a copy from ~/DevPriv/PythonProjects/MediaWikiMgmt/jk_mediawikirepo/src/jk_mediawikirepo/app/*


import sys
import os
import typing

import jk_json
import jk_logging
import jk_typing
import jk_utils
import jk_argparsing
import jk_version

from .OutputWriter import OutputWriter
from .CLICmdBase import CLICmdBase
from .CLICmdParams import CLICmdParams







class AbstractCLIApp(object):

	################################################################################################################################
	## Constructor Methods
	################################################################################################################################

	def __init__(self):
		mainModule = jk_utils.python.getMainModule()
		assert mainModule

		mainScriptFilePath = os.path.realpath(mainModule.__file__)
		self.__mainScriptVersion = jk_version.Version(mainModule.__version__)

		self.__appName = os.path.basename(mainScriptFilePath)
		pos = self.__appName.rfind(".")
		assert pos > 0
		self.__appName = self.__appName[:pos]
		self.__cliBaseDir = os.path.dirname(mainScriptFilePath)

		self.__userCfgDirPath = os.path.join(jk_utils.users.getUserHome(), ".config", self.__appName)

		self.__systemCfgDirPath = os.path.join("/etc", self.__appName)

		self.__cmds = {}
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def appName(self) -> str:
		return self.__appName
	#

	@property
	def userCfgDirPath(self) -> str:
		return self.__userCfgDirPath
	#

	@property
	def userCfgFilePath(self) -> str:
		return os.path.join(self.__userCfgDirPath, "cfg.jsonc")
	#

	@property
	def systemCfgDirPath(self) -> str:
		return self.__systemCfgDirPath
	#

	@property
	def systemCfgFilePath(self) -> str:
		return os.path.join(self.__systemCfgDirPath, "cfg.jsonc")
	#

	#
	# The directory of the main CLI script. This is the python script that is launched by python, which in turn instantiates AbstractCLIApp.
	#
	@property
	def cliBaseDir(self) -> str:
		return self.__cliBaseDir
	#

	#
	# All command objects registered
	#
	@property
	def cmds(self) -> typing.List[CLICmdBase]:
		return list(self.__cmds.values())
	#

	#
	# All command objects registered
	#
	@property
	def cmdNames(self) -> typing.List[str]:
		return list(self.__cmds.keys())
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __processCfg_list(self, jCfgList:list):
		for i, v in enumerate(jCfgList):
			if isinstance(v, str):
				if v.startswith("~/"):
					v = os.path.join(jk_utils.users.getUserHome(), v[2:])
					v[i] = v
			elif isinstance(v, dict):
				self.__processCfg_dict(v)
			elif isinstance(v, list):
				self.__processCfg_list(v)
	#

	def __processCfg_dict(self, jCfg:dict):
		for k, v in jCfg.items():
			if isinstance(v, str):
				if v.startswith("~/"):
					v = os.path.join(jk_utils.users.getUserHome(), v[2:])
					jCfg[k] = v
			elif isinstance(v, dict):
				self.__processCfg_dict(v)
			elif isinstance(v, list):
				self.__processCfg_list(v)
	#

	################################################################################################################################
	## Methods to Override
	################################################################################################################################

	def shortAppDescriptionImpl(self) -> str:
		raise NotImplementedError()
	#

	def shortAppParamInfoImpl(self) -> str:
		raise NotImplementedError()
	#

	def initializeImpl(self, ap:jk_argparsing.ArgsParser, log:jk_logging.AbstractLogger):
		pass
	#

	def createLoggerImpl(self) -> jk_logging.AbstractLogger:
		jk_logging.COLOR_LOG_MESSAGE_FORMATTER.setOutputMode(jk_logging.ColoredLogMessageFormatter.EnumOutputMode.FULL)
		log = jk_logging.ConsoleLogger.create(logMsgFormatter=jk_logging.COLOR_LOG_MESSAGE_FORMATTER)
		return log
	#

	def configurationOptionKeysImpl(self) -> typing.List[str]:
		return []
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def initialize(self, log:jk_logging.AbstractLogger) -> jk_argparsing.ArgsParser:
		# initialize argument parser

		ap = jk_argparsing.ArgsParser(
			self.appName + " " + self.shortAppParamInfoImpl(),
			self.shortAppDescriptionImpl()
			)

		# set defaults

		ap.optionDataDefaults.set("bShowHelp", False)
		ap.optionDataDefaults.set("bShowVersion", False)

		ap.optionDataDefaults.set("bVerbose", False)
		ap.optionDataDefaults.set("bSimulate", False)
		ap.optionDataDefaults.set("bForce", False)

		# arguments

		ap.createOption("h", "help", "Display this help text and then exit.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: parsedArgs.optionData.set("bShowHelp", True)
		ap.createOption(None, "version", "Display the version of this software and then exit.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: parsedArgs.optionData.set("bShowVersion", True)
		ap.createOption("v", "verbose", "Generate verbose output.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: parsedArgs.optionData.set("bVerbose", True)
		ap.createOption("f", "force", "Enforce changes though there might be some aspects inappropriate for such kind of action.").onOption = \
			lambda argOption, argOptionArguments, parsedArgs: parsedArgs.optionData.set("bForce", True)

		# not used right now
		#ap.createOption("s", "simulate", "Simulate the specified action instead of performing it.").onOption = \
		#	lambda argOption, argOptionArguments, parsedArgs: parsedArgs.optionData.set("bSimulate", True)

		# return codes

		ap.createReturnCode(0, "Operation successfully completed.")
		ap.createReturnCode(1, "An error occurred.")

		self.initializeImpl(ap, log)

		for cmd in self.__cmds.values():
			cmd.registerCmd(ap)

		return ap
	#

	#
	# This is a very primitive version of merging two configurations. You might overwrite this method to provide a more sophisticated one.
	#
	def loadConfiguration(self, programArgOptionData:dict, optionKeys:list) -> dict:
		d1 = self.loadSystemConfiguration()
		d2 = self.loadUserConfiguration()

		d = {} if d1 is None else d1
		if d2:
			d.update(d2)

		for k in optionKeys:
			if k in programArgOptionData:
				d[k] = programArgOptionData[k]

		self.__processCfg_dict(d)

		return d
	#

	def loadUserConfiguration(self) -> dict:
		if os.path.isfile(self.userCfgFilePath):
			return jk_json.loadFromFile(self.userCfgFilePath)
		else:
			return None
	#

	def loadSystemConfiguration(self) -> dict:
		if os.path.isfile(self.systemCfgFilePath):
			return jk_json.loadFromFile(self.systemCfgFilePath)
		else:
			return None
	#

	def getCmd(self, cmdName:str) -> typing.Union[CLICmdBase,None]:
		return self.__cmds.get(cmdName)
	#

	#
	# Use this method to register a command before further use.
	#
	def registerCLICmd(self, cmd:CLICmdBase, log:jk_logging.AbstractLogger):
		#assert isinstance(devonlet, DevonletBase)		# circular reference problem
		assert cmd.cmdName not in self.__cmds

		if log:
			log.notice("Registering command " + repr(cmd.cmdName))

		self.__cmds[cmd.cmdName] = cmd
	#

	def run(self):
		# initialize logger

		log = self.createLoggerImpl()

		# initialize

		blog = jk_logging.BufferLogger.create()
		bInitSuccess = False
		try:
			with blog.descend("Initializing ...") as log2:
				ap = self.initialize(log2)

			# process command line arguments
			with blog.descend("Parsing command line ...") as log2:
				parsedArgs = ap.parse()

				if parsedArgs.optionData["bVerbose"]:
					parsedArgs.dump(printFunction=log2.notice)

			# loading configuration
			with blog.descend("Loading configuration ...") as log2:
				jCfg = self.loadConfiguration(parsedArgs.optionData, self.configurationOptionKeysImpl())

				if parsedArgs.optionData["bVerbose"]:
					for k, v in jCfg.items():
						log2.notice(k + " = " + ("(null)" if v is None else str(v)))

			bInitSuccess = True
		except jk_logging.ExceptionInChildContextException as ee:
			pass
		except Exception as ee:
			blog.error(ee)

		if not bInitSuccess:
			blog.forwardTo(log)
			sys.exit(1)
		elif parsedArgs.optionData["bVerbose"]:
			blog.forwardTo(log)

		try:
			if parsedArgs.optionData["bShowVersion"]:
				print()
				print(self.__mainScriptVersion)
				sys.exit(1)

			if parsedArgs.optionData["bShowHelp"]:
				print()
				ap.showHelp()
				sys.exit(1)

			if len(parsedArgs.programArgs) == 0:
				print()
				ap.showHelp()
				sys.exit(1)

			# parse all commands, one by one

			while True:
				try:
					(cmdName, cmdArgs) = parsedArgs.parseNextCommand()
				except Exception as e:
					log.error(str(e))
					sys.exit(1)

				if cmdName is None:
					break

				if cmdName == "help":
					ap.showHelp()
					break

				cmd = self.getCmd(cmdName)
				if cmd:
					ctx = CLICmdParams(
						self,
						cmdArgs,
						jCfg,
						parsedArgs.optionData["bVerbose"],
						parsedArgs.optionData["bSimulate"],
						parsedArgs.optionData["bForce"],
						)

					cmd.run(ctx, log)
					break

				log.error("Unknown command: " + repr(cmdName))
				sys.exit(1)

		except jk_logging.ExceptionInChildContextException as ee:
			sys.exit(1)
		except Exception as ee:
			log.exception(ee)
			sys.exit(1)
	#

#






