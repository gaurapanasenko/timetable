import datetime

from django.conf import settings

START_YEAR = getattr(settings, 'TIMETABLEAPP_START_YEAR', 1900)
FUTURE_DIFF = getattr(settings, 'TIMETABLEAPP_FUTURE_DIFF', 5)
MAX_LESSONS_DAY = getattr(settings, 'TIMETABLEAPP_MAX_LESSONS_DAY', 5)
WORK_DAYS = getattr(settings, 'TIMETABLEAPP_WORK_DAYS', [0, 1, 2, 3, 4, 5])
MAX_GROUP_TREE_HEIGHT = getattr(settings, 'TIMETABLEAPP_MAX_GROUP_TREE_HEIGHT', 3)

def current_year():
    return datetime.date.today().year
