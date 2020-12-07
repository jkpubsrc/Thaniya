

import typing
import re
import time
import os
import random

import jk_utils
import jk_json







#
# This class represents a backup data file. Backup data files form the main data content of a backup.
#
class BackupDataFile(object):

	################################################################################################################################
	## Constructors
	################################################################################################################################

	def __init__(self, fe):
		self.__fileName = fe.name
		self.__filePath = fe.path
		self.__size = jk_utils.AmountOfBytes.parse(fe.stat().st_size)
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	@property
	def filePath(self) -> str:
		return self.__filePath
	#

	@property
	def fileName(self) -> str:
		return self.__fileName
	#

	@property
	def sizeInBytes(self) -> jk_utils.AmountOfBytes:
		return self.__size
	#

	################################################################################################################################
	## Static Methods
	################################################################################################################################

#















