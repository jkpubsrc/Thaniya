



import typing
import time
import threading

import jk_typing

from .SessionIDGenerator import SessionIDGenerator







#
# This is a general purpose in memory session manager. It holds all session data in memory.
# 
# This object stores the following data indexed by the sessionID:
#
# * <c>any sessionID</c> : The session identifier. This data value must be readonly and hashable. You might want to use an integer or string value for this purpose.
#		As the security of sessions relies on the knowledge of this identifier make this identifier sufficiently random in order to avoid
#		guessing. Do *not* rely on time stamps for this identifier!
# * <c>float timeStamp</c> : The time stamp of lasst access in seconds since Epoch. This time stamp is used to calculate the age of the session. If it is larger than
#		the allowed age the session is invalidated.
# * <c>any fingerprint</c> : The fingerprint that is generated from connection data from a client. All future <c>get()</c> requests must be equal to this fingerprint.
#		You might want to use some kind of string or binary value here.
#		Have in mind that a fingerprint should be read only and must be testable for equality. If you provde a custom object here it therefore should
#		implement <c>__eq__()</c>.
# * <c>any userName</c> : The user name to register with the session identifier.
# 		You might want to use an integer or string user identifier here but in theory you could as well provide the user object itself.
#		Please have in mind that storing a user object over a longer period of time might raise problems with having outdated user objects
#		left here in memory while the user data has already been updated in some kind of database.
#		Please have in mind that this object is simply left to garbace collection if a session is invalidated.
# * <c>any sessionData</c>: The session data to register with the session identifier.
#		You might want to provide a dictionary here but in theory you could provide any object you like.
#		Please have in mind that this object is simply left to garbace collection if a session is invalidated.
#
# Please call <c>cleanup()</c> frequently in order to invalidate sessions that are timed out. Depending on the work load invoking this method every 30 seconds or even
# every minute might be sufficient as a call to <c>get()</c> will check for timeout on a particular session anyway.
#
# This class is thread safe. You may safely use it in a multithreaded environment.
#
class MemorySessionManager(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, timeOutSeconds:int):
		assert timeOutSeconds > 0

		# ----

		self.__timeOutSeconds = timeOutSeconds
		self.__data = {}
		self.__lock = threading.Lock()
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

	#
	# Check for sessions that have timed out. If sessions are found that have timed out the session is removed and all data is left to garbage collection
	# without any further notice.
	#
	def cleanup(self):
		with self.__lock:
			keysToRemove = []

			tNow = time.time()
			for _id, _t, _fingerprint, _userName, _sessionData  in self.__data.values():
				if tNow - _t > self.__timeOutSeconds:
					keysToRemove.append(_id)

			for identifier in keysToRemove:
				del self.__data[identifier]
	#

	#
	# Register a new session.
	#
	# @param		any identifier		The session identifier. This data value must be readonly and hashable.
	#									You might want to use an integer or string session identifier here.
	#									As the security of sessions relies on the knowledge of this identifier make this identifier sufficiently random in order to avoid
	#									guessing. Do *not* rely on time stamps for this identifier!
	# @param		any fingerprint		The fingerprint that is generated from connection data from a client. All future <c>get()</c> requests must be equal to this fingerprint.
	#									You might want to use some kind of string or binary value here.
	#									Have in mind that a fingerprint should be read only and must be testable for equality. If you provde a custom object here it therefore should
	#									implement <c>__eq__()</c>.
	# @param		any userName		The user name to register with the session identifier.
	#									You might want to use an integer or string user identifier here but in theory you could as well provide the user object itself.
	#									Please have in mind that storing a user object over a longer period of time might raise problems with having outdated user objects
	#									left here in memory while the user data has already been updated in some kind of database.
	#									Please have in mind that this object is simply left to garbace collection if a session is invalidated.
	# @param		any sessionData		The session data to register with the session identifier.
	#									You might want to provide a dictionary here but in theory you could provide any object you like.
	#									Please have in mind that this object is simply left to garbace collection if a session is invalidated.
	#
	def put(self, identifier, fingerprint, userName, sessionData):
		assert identifier is not None
		assert fingerprint is not None
		assert sessionData is not None
		assert userName is not None

		with self.__lock:
			self.__data[identifier] = [ identifier, time.time(), fingerprint, userName, sessionData ]
	#

	#
	# Invalidate an existing session.
	#
	def invalidate(self, identifier):
		assert identifier is not None

		with self.__lock:
			if identifier in self.__data:
				del self.__data[identifier]
	#

	#
	# Retrieve an existing session.
	#
	# NOTE: The session is checked for timeout. If a timeout has occured the session is invalidated and *not* returned.
	#
	# @param		any identifier		The session identifier. (For more information to session identifiers please see the documentation for <c>put()</c>.)
	# @param		any fingerprint		The fingerprint that is generated from connection data from a client. This fingerprint specified here must match the fingerprint
	#									provided for <c>put()</c>. If the fingerprints don't match the users are considered as being different though the session ID might be correct.
	#									This mechanism ensures that it's more difficult for other users to guess or reuse a session ID.
	# @param		bool bTouch			If <c>True</c> is specified a new current time stamp is stored if <c>get()</c> succeeds this way effectively renewing the session.
	#
	# @return		userName			Returns the user name associated with the identifier. <c>None</c> is returned if the session is invalid.
	# @return		sessionData			Returns the session data associated with the identifier. <c>None</c> is returned if the session is invalid.
	#
	def get(self, identifier, fingerprint, bTouch:bool) -> tuple:
		assert identifier is not None
		assert fingerprint is not None
		assert isinstance(bTouch, bool)

		with self.__lock:
			r = self.__data.get(identifier)
			if r is None:
				return None, None

			_id, _t, _fingerprint, _userName, _sessionData = r

			tNow = time.time()
			if tNow - _t > self.__timeOutSeconds:
				del self.__data[identifier]
				return None, None
			
			if _fingerprint != fingerprint:
				return None, None

			if bTouch:
				r[1] = tNow

			return _userName, _sessionData
	#

#





























