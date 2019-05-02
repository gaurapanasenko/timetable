import calendar

from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from django.core.validators import ValidationError

from .helpers import YearlessDate

DAY_CHOICES = tuple([('', '---------' )] + [(i,i) for i in range(1,32)])
MONTH_CHOICES = tuple([('', '---------' )] + [(i, calendar.month_name[i]) for i in range(1,13)])


class YearlessDateSelect(widgets.MultiWidget):
    def __init__(self, attrs = None):
        _widgets = (
            widgets.Select(attrs=attrs, choices=MONTH_CHOICES),
            widgets.Select(attrs=attrs, choices=DAY_CHOICES),
        )
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value is None:
            return [None, None]
        return [value.month, value.day]

class YearlessDateField(forms.Field):
    widget = YearlessDateSelect

    def clean(self, value):
        if value == ['', '']:
            super(YearlessDateField, self).clean(None)
        else:
            try:
                return YearlessDate(*value)
            except:
                raise ValidationError(_('Invalid date.'))
