#!/usr/bin/python3



import typing
import os

import jk_prettyprintobj






class InUseFlag(jk_prettyprintobj.DumpMixin):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor method.
	#
	def __init__(self, identifier = None):
		self.__identifier = identifier
		self.__counter = 0
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def identifier(self):
		return self.__identifier
	#

	@property
	def isInUse(self) -> bool:
		return self.__counter > 0
	#

	@property
	def usageCounter(self) -> int:
		return self.__counter
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def _dumpVarNames(self) -> list:
		return [
			"identifier",
			"isInUse",
			"usageCounter",
		]
	#

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







