

import typing

import jk_sysinfo
import jk_typing
import jk_json







class _Matcher(object):

	def __init__(self, key:str, value, dataType:type):
		assert isinstance(dataType, type)
		self.dataType = dataType

		assert isinstance(key, str)
		self.key = key

		if isinstance(value, (tuple,list)):
			for x in value:
				assert isinstance(x, dataType)
			self.values = value
		else:
			assert isinstance(value, dataType)
			self.values = [ value ]
	#

	def match(self, jDict:dict) -> bool:
		v = jDict.get(self.key, None)
		if v is not None:
			assert isinstance(v, self.dataType)
			if v in self.values:
				return True
		return False
	#

#



class ProcessFilter(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	def __init__(self, userName:str = None, groupName:str = None, uid:int = None, gid:int = None, pid:int = None, ppid:int = None, cmd:str = None, cwd:str = None, args:str = None,
		userNameMatcher = None, groupNameMatcher = None, cmdMatcher = None, argsMatcher = None):

		self.__matchers = []

		if userName is not None:
			assert isinstance(userName, str)
			#print("userName matcher:", userName)
			self.__matchers.append(_Matcher("user", userName, str))

		if groupName is not None:
			assert isinstance(groupName, str)
			#print("groupName matcher:", groupName)
			self.__matchers.append(_Matcher("group", groupName, str))

		if uid is not None:
			assert isinstance(uid, int)
			assert uid >= 0
			#print("uid matcher:", uid)
			self.__matchers.append(_Matcher("uid", uid, int))

		if gid is not None:
			assert isinstance(gid, str)
			assert gid >= 0
			#print("gid matcher:", gid)
			self.__matchers.append(_Matcher("gid", gid, int))

		if pid is not None:
			assert isinstance(pid, int)
			#print("ppid matcher:", ppid)
			self.__matchers.append(_Matcher("pid", pid, int))

		if ppid is not None:
			assert isinstance(ppid, str)
			assert ppid > 0
			#print("ppid matcher:", ppid)
			self.__matchers.append(_Matcher("ppid", ppid, int))

		if cmd is not None:
			assert isinstance(cmd, str)
			#print("cmd matcher:", cmd)
			self.__matchers.append(_Matcher("cmd", cmd, str))

		if cwd is not None:
			assert isinstance(cwd, str)
			#print("cwd matcher:", cwd)
			self.__matchers.append(_Matcher("cwd", cwd, str))

		if args is not None:
			assert isinstance(args, str)
			#print("args matcher:", args)
			self.__matchers.append(_Matcher("args", args, str))

		if userNameMatcher is not None:
			assert callable(userNameMatcher)

		if groupNameMatcher is not None:
			assert callable(groupNameMatcher)

		if cmdMatcher is not None:
			assert callable(cmdMatcher)

		if argsMatcher is not None:
			assert callable(argsMatcher)

		self.__userName = userName
		self.__groupName = groupName
		self.__uid = uid
		self.__gid = gid
		self.__pid = pid
		self.__ppid = ppid
		self.__cmd = cmd
		self.__cwd = cwd
		self.__args = args

		self.__userNameMatcher = userNameMatcher
		self.__groupNameMatcher = groupNameMatcher
		self.__cmdMatcher = cmdMatcher
		self.__argsMatcher = argsMatcher
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def findProcessStructs(self) -> list:
		result = []
		for jDict in jk_sysinfo.get_ps():
			bReject = False
			for m in self.__matchers:
				if not m.match(jDict):
					bReject = True
					break
			if bReject:
				continue

			if self.__userNameMatcher:
				if not self.__userNameMatcher(jDict.get("user", None)):
					continue

			if self.__groupNameMatcher:
				if not self.__groupNameMatcher(jDict.get("group", None)):
					continue

			if self.__cmdMatcher:
				if not self.__cmdMatcher(jDict.get("cmd", None)):
					continue

			if self.__argsMatcher:
				if not self.__argsMatcher(jDict.get("args", None)):
					continue

			result.append(jDict)

		return result
	#

#











