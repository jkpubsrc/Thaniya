



import jk_prettyprintobj
from jk_utils.typed import TypedList






class BackupUser(jk_prettyprintobj.DumpMixin):

	# @field		str userName			The name of this user.
	# @field		str passwordHash		The password hash of this user.
	# @field		str eMail				The EMail address of this user.
	# @field		bool enabled			Is the user enabled? If not logins are prohibited.
	# @field		str comment				A comment field for administrators. Currently unused.
	# @field		str role				A role field. Currently unused.
	# @field		str uploadPwd			If set this contains an extra password unhashed and in plaintext that
	#										clients may use to connect to the API and perform an upload.
	# @field		str[] supervises		Specifies other users this user might supervise.

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self):
		self._userMgr = None

		self.userName = None
		self.passwordHash = None
		self.eMail = None
		self.enabled = False
		self.comment = None
		self.role = None
		self.uploadPwd = None
		self.supervises = None

		#self.backup_accountName = None
		#self.backup_lastActivity = -1
		#self.backup_sessionID = None
	#

	################################################################################################################################
	## Flask Properties
	################################################################################################################################

	#
	# Used by flask_login:
	# The login name of the user. This is a unique identificator.
	#
	@property
	def name(self) -> str:
		#print(">> name()")
		return self.userName
	#

	#
	# Used by flask_login:
	# Is the user account enabled or disabled?
	#
	@property
	def is_active(self) -> bool:
		#print(">> is_active()")
		return self.enabled
	#

	#
	# Used by flask_login:
	# Is this an anonymous user?
	#
	@property
	def is_anonymous(self) -> bool:
		#print(">> is_anonymous()")
		return False
	#

	#
	# Used by flask_login:
	# Has the user completed the registration process an is ready for login?
	#
	@property
	def is_authenticated(self) -> bool:
		#print(">> is_authenticated()")
		return True
	#

	#
	# Used by flask_login:
	# The user's email address
	#
	@property
	def email(self) -> str:
		#print(">> email()")
		return self.eMail
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def canUpload(self) -> bool:
		return bool(self.uploadPwd)
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"userName",
			"passwordHash",
			"eMail",
			"enabled",
			"comment",
			"role",
			"uploadPwd",
			"supervises",

			#"backup_accountName",
			#"backup_lastActivity",
			#"backup_sessionID",
		]
	#

	################################################################################################################################
	## Flask Methods
	################################################################################################################################

	#
	# This method is invoked by flask-login to obtain the user's identificator.
	#
	def get_id(self) -> str:
		#print(">> get_id()")
		return self.userName
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def hasPrivilege(self, privilegeName:str) -> bool:
		if self._userMgr:
			return self._userMgr.hasPrivilege(self, privilegeName)
		else:
			return False
	#

	def toJSON(self) -> dict:
		return self.serialize()
	#

	def deserialize(self, ctx, jData:dict):
		self.userName = jData.get("userName")
		self.passwordHash = jData.get("passwordHash")
		self.eMail = jData.get("eMail")
		self.enabled = jData.get("enabled")
		self.comment = jData.get("comment")
		self.role = jData.get("role")
		self.uploadPwd = jData.get("uploadPwd")
		self.supervises = TypedList(items=jData.get("supervises"), dataType=str)

		#self.backup_accountName = jData.get("backup_accountName")
		#self.backup_lastActivity = jData.get("backup_lastActivity")
		#self.backup_sessionID = jData.get("backup_sessionID")
	#

	def serialize(self, ctx) -> dict:
		return {
			"userName": self.userName,
			"passwordHash": self.passwordHash,
			"eMail": self.eMail,
			"enabled": self.enabled,
			"comment": self.comment,
			"role": self.role,
			"uploadPwd": self.uploadPwd,
			"supervises": self.supervises,

			#"backup_accountName": self.backup_accountName,
			#"backup_lastActivity": self.backup_lastActivity,
			#"backup_sessionID": self.backup_sessionID,
		}
	#

	def __eq__(self, other):
		if isinstance(other, BackupUser):
			return other.userName == self.userName
		else:
			return False
	#

	def __ne__(self, other):
		if isinstance(other, BackupUser):
			return other.userName != self.userName
		else:
			return False
	#

	def __gt__(self, other):
		if isinstance(other, BackupUser):
			return self.userName > other.userName
		else:
			return False
	#

	def __ge__(self, other):
		if isinstance(other, BackupUser):
			return self.userName >= other.userName
		else:
			return False
	#

	def __lt__(self, other):
		if isinstance(other, BackupUser):
			return self.userName < other.userName
		else:
			return False
	#

	def __le__(self, other):
		if isinstance(other, BackupUser):
			return self.userName <= other.userName
		else:
			return False
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#
























