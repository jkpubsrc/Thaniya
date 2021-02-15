

__version__ = "0.2021.2.15"



from .FlaskFilter_boolToYesNo import FlaskFilter_boolToYesNo
from .FlaskFilter_formatBytes import FlaskFilter_formatBytes
from .FlaskFilter_formatDate import FlaskFilter_formatDate
from .FlaskFilter_formatDateTime import FlaskFilter_formatDateTime
from .FlaskFilter_formatDateTimeHRAge import FlaskFilter_formatDateTimeHRAge
from .FlaskFilter_formatPercent import FlaskFilter_formatPercent
from .FlaskFilter_j import FlaskFilter_j
from .FlaskFilter_listToStr import FlaskFilter_listToStr
from .FlaskFilter_strToID import FlaskFilter_strToID
from .FlaskFilter_tagsColoredToStr import FlaskFilter_tagsColoredToStr
from .FlaskFilter_tagsToStr import FlaskFilter_tagsToStr
from .FlaskFilter_toStr import FlaskFilter_toStr
from .FlaskFilter_formatTime import FlaskFilter_formatTime
from .FlaskFilter_formatDateHR import FlaskFilter_formatDateHR




ALL_FLASK_FILTER_CLASSES = [
	FlaskFilter_boolToYesNo,
	FlaskFilter_formatBytes,
	FlaskFilter_formatDate,
	FlaskFilter_formatDateHR,
	FlaskFilter_formatDateTime,
	FlaskFilter_formatDateTimeHRAge,
	FlaskFilter_formatTime,
	FlaskFilter_formatPercent,
	FlaskFilter_j,
	FlaskFilter_listToStr,
	FlaskFilter_strToID,
	FlaskFilter_tagsColoredToStr,
	FlaskFilter_tagsToStr,
	FlaskFilter_toStr,
]