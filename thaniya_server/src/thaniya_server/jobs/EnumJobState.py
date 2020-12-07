

import os
import typing
import enum







#
# This class is a generic job used at runtime. It is managed by the job queue.
#
class EnumJobState(enum.Enum):

	READY = "ready"
	PROCESSING = "processing"
	SUCCESS = "success"
	SUSPENDED = "suspended"
	INTERRUPTED = "interrupted"
	ERROR = "error"
	ERR_UNKNOWN = "err_unknown"

#


















