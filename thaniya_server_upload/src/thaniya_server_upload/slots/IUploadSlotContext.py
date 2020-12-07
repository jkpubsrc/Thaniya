


from thaniya_server_sudo import SudoScriptRunner
from thaniya_server.usermgr import BackupUserManager
from thaniya_server.sysusers import SystemAccountManager




class IUploadSlotContext:

	@property
	def backupUserManager(self) -> BackupUserManager:
		raise NotImplementedError()
	#

	@property
	def sudoScriptRunner(self) -> SudoScriptRunner:
		raise NotImplementedError()
	#

	@property
	def systemAccountManager(self) -> SystemAccountManager:
		raise NotImplementedError()
	#

#






