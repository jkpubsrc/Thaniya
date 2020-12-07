#!/usr/bin/python3



import typing
import os
import sys

import jk_json
import jk_utils






class InUseFlag(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, identifier):
		self.__identifier = identifier
		self.__counter = 0
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def identifier(self) -> str:
		return self.__identifier
	#

	@property
	def isInUse(self) -> bool:
		return self.__counter > 0
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	#
	# This method is invoked if the context is entered.
	#
	def __enter__(self):
		# print(self.__name, ": __enter__() :", self.__counter, "->", self.__counter + 1)
		self.__counter += 1
		return self
	#

	#
	# This method is invoked if the context is terminated.
	#
	# NOTE: Never raise an exception within <c>__exit__()</c>.
	#
	# @param		type exType		The type of the exception. (This is the class of the exception.) <c>None</c> is passed no exception occurred and everything went well.
	# @param		obj ex			The exception object (if raised). <c>None</c> is passed no exception occurred and everything went well.
	# @param		traceback		A traceback object that represents the stack trace of the exception. <c>None</c> is passed no exception occurred and everything went well.
	# @return		bool			If <c>True</c> is returned this method handled the exception. The exception is then swallowed. If <c>None</c> (= nothing, no return
	#								statement) is returned the exception will be handled by the Python framework after <c>__exit__()</c> returned.
	#
	def __exit__(self, exType, ex, traceback):
		# print(self.__name, ": __exit__() :", self.__counter, "->", self.__counter - 1)
		if self.__counter == 0:
			raise Exception("Zero underrun!")
		self.__counter -= 1
	#

	def allocate(self):
		self.__counter += 1
	#

	def deallocate(self):
		if self.__counter == 0:
			raise Exception("Zero underrun!")
		self.__counter -= 1
	#

#



class InUseManager(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self):
		self.__inUseFlags = {}
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def get(self, identifier) -> InUseFlag:
		assert identifier is not None

		if identifier in self.__inUseFlags:
			f = self.__inUseFlags[identifier]
		else:
			f = InUseFlag(identifier)
			self.__inUseFlags[identifier] = f

		return f
	#

	def discard(self, identifier):
		assert identifier is not None

		if identifier in self.__inUseFlags:
			f = self.__inUseFlags[identifier]
			if f.isInUse:
				raise Exception("Can't discard objects still in use: " + str(f.identifier))
			else:
				del self.__inUseFlags[identifier]
	#

	def __del__(self, identifier):
		self.discard(identifier)
	#

#



inUseMgr = InUseManager()
fooFlag = inUseMgr.get("foo")

with fooFlag:
	print("~~~~1")
	print("~~>", fooFlag.isInUse)

print()
print(">", fooFlag.isInUse)
print()

with fooFlag:
	with fooFlag:
		print("~~~~2")
		print("~~>", fooFlag.isInUse)

print()
print(">", fooFlag.isInUse)
print()












