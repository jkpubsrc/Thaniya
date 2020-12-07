

import time
import binascii
import base64




# DataStoreIDs			uniquely identify a data store.
# ObjectIDs				uniquely identify a data object.
# RevisionIDs			identify a revision of an object.
# ObjectRevisionIDs		uniquely identify a specific revision of a specific object.
# DataCollectionIDs		uniquely identify a specific collection of objects.
# ClassIDs				uniquely identify type of an object.



# DataStoreIDs			are 4 bytes (= 32 bits) in length		and generated with random data
# SyncGroupIDs			are 128 bytes (= 1024 bits) in length	and generated with random data
# ObjectIDs				are 12 bytes (= 96 bits) in length		and a concatenation of a DataStoreID and an enumeration starting by 1
# RevisionIDs			are 12 bytes (= 96 bits) in length		and based on a time stamp
# ObjectInstanceIDs		are 24 bytes (= 192 bits) in length		and a concatenation of a ObjectID and a RevisionID
# DataCollectionIDs		are 12 bytes (= 96 bits) in length		and a concatenation of random data
# ClassIDs				are 8 bytes (= 64 bits) in length		and a concatenation of random data
# ClassRevisionIDs		are 8 bytes (= 64 bits) in length		and a concatenation of random data






#
# Abstract base class for all IDs
#
class ID(object):

	#
	# Initialization method.
	#
	# @param	int byteLength			The length of this ID in bytes.
	# @param	mixed idData			The data of this ID. This is either of type <c>byte[]</c> or of type <c>str</c>.
	#									The binary data is the direct representation of the ID in big endian byte order which means:
	#									the highest part of the data value is stored at position <c>0</c>, the lowest part on position <c>byteLength - 1</c>
	#
	def __init__(self, byteLength, idData):
		assert isinstance(byteLength, int)
		assert byteLength > 0
		assert isinstance(idData, (str, bytes, bytearray))

		self.__byteLength = byteLength
		self.__idData = ID._toByteArray(byteLength, idData)
	#

	def __hash__(self):
		#return self.__idData.__hash__()
		return hash((self.__class__.__name__, self.__idData))
	#

	#
	# Get the current time in nanoseconds since 1.1.1970 00:00:00
	#
	@staticmethod
	def _getCurrentTimeNanos():
		return int(time.time() * 1000000)	# currently using 13 hex digits
	#

	#
	# Get the current time in milliseconds since 1.1.1970 00:00:00
	#
	@staticmethod
	def _getCurrentTimeMillis():
		return int(time.time() * 1000)	# currently using 11 hex digits
	#

	@staticmethod
	def _getCurrentTimeMillisAsBytes():
		return int(time.time() * 1000).to_bytes(8, byteorder='big')
	#

	@staticmethod
	def _getCurrentTimeNanosAsBytes():
		return int(time.time() * 1000000).to_bytes(8, byteorder='big')
	#

	@staticmethod
	def _getCurrentTimeNanosAsBytesWithSpecial():
		return int(time.time() * (1000000 * 256)).to_bytes(8, byteorder='big')
	#

	@staticmethod
	def _toByteArray(byteLength, idData):
		if isinstance(idData, str):
			idData = bytes(binascii.unhexlify(idData))
		elif isinstance(idData, bytearray):
			idData = bytes(idData)
		elif isinstance(idData, bytes):
			pass
		else:
			raise Exception(str(type(idData)))
		assert len(idData) == byteLength
		return idData
	#

	@property
	def byteLength(self):
		return self.__byteLength
	#

	@property
	def binaryData(self):
		return self.__idData
	#

	@property
	def hexData(self):
		return str(binascii.hexlify(self.__idData).decode())
	#

	@property
	def base64Data(self):
		return str(base64.b64encode(self.__idData).decode())
	#

	@property
	def typeName(self):
		return self.__class__.__name__
	#

	def __eq__(self, other):
		if other is None:
			return False
		# if self.typeName != other.typeName:
		#	return False
		#if self.__byteLength != len(other.__id):
		#	return False
		#for n in range(self.__byteLength):
		#	if self.__idData[n] != other.__id[n]:
		#		return False
		#return True
		if self.__class__.__name__ == other.__class__.__name__:
			return self.__idData == other.__idData
		else:
			return False
	#

	def __ne__(self, other):
		if other is None:
			return True
		#if self.typeName != other.typeName:
		#	return True
		#if self.__byteLength != len(other.__id):
		#	return True
		#for n in range(self.__byteLength):
		#	if self.__idData[n] != other.__id[n]:
		#		return True
		#return False
		#return not (self.typeName, self.__byteLength, self.__idData) == (other.typeName, other.__byteLength, other.__idData)
		if self.__class__.__name__ != other.__class__.__name__:
			return True
		else:
			return self.__idData != other.__idData
	#

	def compareTo(self, other):
		if other is None:
			return -1
		if self.typeName != other.typeName:
			return -1 if self.typeName < other.typeName else 1
		if self.__byteLength != len(other.__idData):
			return -1 if self.__byteLength < len(other.__idData) else 1
		for n in range(self.__byteLength):
			if self.__idData[n] != other.__idData[n]:
				return -1 if self.__idData[n] < other.__idData[n] else 1
		return 0
	#

	def __len__(self):
		return self.byteLength
	#

	def __bytes__(self):
		return self.__idData
	#

	def __gt__(self, other):
		n = self.compareTo(other)
		return n > 0
	#

	def __ge__(self, other):
		n = self.compareTo(other)
		return n >= 0
	#

	def __lt__(self, other):
		n = self.compareTo(other)
		return n < 0
	#

	def __le__(self, other):
		n = self.compareTo(other)
		return n <= 0
	#

	def __str__(self):
		return self.__class__.__name__ + "(<" + binascii.hexlify(self.__idData).decode() + ">)"
	#

	def __repr__(self):
		return self.__class__.__name__ + "(<" + binascii.hexlify(self.__idData).decode() + ">)"
	#

	def isEmpty(self):
		for n in range(self.__byteLength):
			if self.__idData[n] != 0:
				return False
		return True
	#

	def isNotEmpty(self):
		for n in range(self.__byteLength):
			if self.__idData[n] != 0:
				return True
		return False
	#

	#
	# Get a big integer representation of the value stored in this ID.
	#
	def toNumericIntValue(self):
		ba = self.__idData
		ret = ba[0]
		for n in range(1, len(ba)):
			ret *= 256
			ret += ba[n]
		return ret
	#

	def toUInt64Value(self):
		ba = self.__idData
		if len(ba) > 8:
			raise Exception("Not a ulong value!")
		while len(ba) < 8:
			ba = bytes(1) + ba
		num = (ba[0] << 56) + (ba[1] << 48) + (ba[2] << 40) + (ba[3] << 32) + (ba[4] << 24) + (ba[5] << 16) + (ba[6] << 8) + ba[7]
		return num
	#

	def toUInt32Value(self):
		ba = self.__idData
		if len(ba) > 4:
			raise Exception("Not a uint value!")
		while len(ba) < 4:
			ba = bytes(1) + ba
		num = (ba[0] << 24) + (ba[1] << 16) + (ba[2] << 8) + ba[3]
		return num
	#

	def toStr(self):
		return self.__str__()
	#

	@staticmethod
	def _parseBinaryFromString(className, text:str):
		assert isinstance(text, str)
		binData = ID._tryParseBinaryFromString(className, text)
		if binData is None:
			raise Exception("Failed to parse: " + text)
		return binData
	#

	@staticmethod
	def _parseHexFromString(className, text:str):
		assert isinstance(text, str)
		binData = ID._tryParseHexFromString(className, text)
		if binData is None:
			raise Exception("Failed to parse: " + text)
		return binData
	#

	@staticmethod
	def _tryParseBinaryFromString(className, text:str):
		assert isinstance(text, str)
		sPrefix = className + "(<"
		sPostfix = ">)"
		if not text.startswith(sPrefix) or not text.endswith(sPostfix):
			#print("---- " + text)
			#print("---- " + sPrefix)
			#print("---- " + sPostfix)
			return None
		text = text[len(sPrefix):]
		text = text[:-len(sPostfix)]
		try:
			binData = binascii.unhexlify(text)
		except:
			return None
		return binData
	#

	@staticmethod
	def _tryParseHexFromString(text:str):
		assert isinstance(text, str)
		try:
			binData = binascii.unhexlify(text)
		except:
			return None
		return binData
	#

#

















