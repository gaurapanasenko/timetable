from django import forms
from django.forms import widgets, fields
from django.utils.translation import ugettext_lazy as _
from django.core.validators import ValidationError

from .helpers import Lesson
from .settings import *

class LessonSelect(widgets.MultiWidget):
    def __init__(self, attrs=None):
        wdgts = (
            widgets.Select(attrs, choices=WEEK_CHOICES),
            widgets.Select(attrs, choices=DAY_CHOICES),
            widgets.Select(attrs, choices=LESSON_CHOICES),
        )
        super(LessonSelect, self).__init__(wdgts, attrs)

    def decompress(self, value):
        return value or ('', '', '')

class LessonField(fields.MultiValueField):
    widget = LessonSelect

    def __init__(self, *args, **kwargs):
        flds = (
            fields.ChoiceField(choices=WEEK_CHOICES),
            fields.ChoiceField(choices=DAY_CHOICES),
            fields.ChoiceField(choices=LESSON_CHOICES),
        )
        super(LessonField, self).__init__(
            fields=flds, require_all_fields=True, *args, **kwargs
        )

    def clean(self, value):
        if value == ['', '', '']:
            super(LessonField, self).clean(None)
        else:
            v = [int(i) for i in value[:]]
            if v[1] not in WORK_DAYS:
                raise ValidationError(_('Invalid day.'))
            if v[2] > MAX_LESSONS_DAY:
                raise ValidationError(_('Invalid lesson number.'))
            return Lesson((v[0], v[1], v[2]))

    def compress(self, data_list):
        if data_list:
            return Lesson(data_list)
        return None
