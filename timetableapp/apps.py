from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class TimetableappConfig(AppConfig):
    name = 'timetableapp'
    verbose_name = _('Timetable Application')
