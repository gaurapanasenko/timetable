import datetime

from django.conf import settings

START_YEAR = getattr(settings, 'TIMETABLEAPP_START_YEAR', 1900)
FUTURE_DIFF = getattr(settings, 'TIMETABLEAPP_FUTURE_DIFF', 5)
MAX_GROUP_TREE_HEIGHT = getattr(settings, 'TIMETABLEAPP_MAX_GROUP_TREE_HEIGHT', 3)
LIST_PER_PAGE = getattr(settings, 'TIMETABLEAPP_LIST_PER_PAGE', 20)

def current_year():
    return datetime.date.today().year
