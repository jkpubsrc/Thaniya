



import jk_utils






class EnumUploadSlotState(jk_utils.EnumBase):

	DEGRADED = -2, "DEGRADED"
	UNKNOWN = -1, "UNKNOWN"
	READY = 0, "READY"
	UPLOADING = 1, "UPLOADING"
	TIMEOUT = 2, "TIMEOUT"
	FINALIZING = 3, "FINALIZING"
	COMPLETED = 4, "COMPLETED"

#

















