


from .ILocalBackupOriginInfo import ILocalBackupOriginInfo




#
# This strategy builds the subdirectory part where to write backups to.
#
class AbstractTargetDirectoryStrategy(object):

	#
	# This method is invoked in order to receive a valid target directory.
	#
	# @param		ILocalBackupOriginInfo originInfo		Information about the origin of this backup.
	# @return		str										Returns a path which indicates where to write the backup to. This return value will be made part of the absolute path to write data to.
	#
	def selectEffectiveTargetDirectory(self, originInfo:ILocalBackupOriginInfo) -> str:
		raise NotImplementedError()
	#

#

