import calendar

from django import forms
from django.forms import widgets, fields
from django.utils.translation import ugettext_lazy as _
from django.core.validators import ValidationError

from .helpers import YearlessDate, YearlessDateRange

DAY_CHOICES = tuple([('', _('Day') )] + [(i,i) for i in range(1,32)])
MONTH_CHOICES = tuple([('', _('Month') )] + [(i, calendar.month_name[i]) for i in range(1,13)])

class YearlessDateSelect(widgets.MultiWidget):
    def __init__(self, attrs = None):
        _widgets = (
            widgets.Select(attrs=attrs, choices=MONTH_CHOICES),
            widgets.Select(attrs=attrs, choices=DAY_CHOICES),
        )
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value is None:
            return ['', '']
        return [value.month, value.day]

class YearlessDateField(forms.Field):
    widget = YearlessDateSelect

    def __init__(self, **kwargs):
        _fields = (
            fields.ChoiceField(choices=MONTH_CHOICES),
            fields.ChoiceField(choices=DAY_CHOICES),
        )
        super().__init__(
            fields=_fields, require_all_fields=True, **kwargs
        )

    def clean(self, value):
        if value == ['', '']:
            super(YearlessDateField, self).clean(None)
        else:
            try:
                return YearlessDate(*value)
            except:
                raise ValidationError(_('Invalid date.'))

class YearlessDateRangeSelect(widgets.MultiWidget):
    template_name = 'forms/widgets/yearlessdaterange.html'

    def __init__(self, attrs = None):
        _widgets = (
            widgets.Select(attrs=attrs, choices=MONTH_CHOICES),
            widgets.Select(attrs=attrs, choices=DAY_CHOICES),
            widgets.Select(attrs=attrs, choices=MONTH_CHOICES),
            widgets.Select(attrs=attrs, choices=DAY_CHOICES),
        )
        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value is None:
            return ['', '', '', '']
        return [
            value.start.month, value.start.day,
            value.end.month, value.end.day
        ]

class YearlessDateRangeField(fields.MultiValueField):
    widget = YearlessDateRangeSelect

    def __init__(self, **kwargs):
        _fields = (
            fields.ChoiceField(choices=MONTH_CHOICES),
            fields.ChoiceField(choices=DAY_CHOICES),
            fields.ChoiceField(choices=MONTH_CHOICES),
            fields.ChoiceField(choices=DAY_CHOICES),
        )
        super().__init__(
            fields=_fields, require_all_fields=True, **kwargs
        )

    def clean(self, value):
        if value == ['', '', '', '']:
            super(YearlessDateRangeField, self).clean(None)
        else:
            try:
                start = YearlessDate(*value[:2])
                end = YearlessDate(*value[2:])
                return YearlessDateRange(start, end)
            except:
                raise ValidationError(_('Invalid date.'))
