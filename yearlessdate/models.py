from django.db import models
from .helpers import YearlessDate, YearlessDateRange
from . import forms

class YearlessDateField(models.Field):
    def to_python(self, value):
        if isinstance(value, YearlessDate):
            return value
        if not value:
            return None
        return YearlessDate(int(value / 32), value % 32)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def db_type(self, connection):
        return 'smallint'

    def get_prep_value(self, value):
        if value is not None:
            return value.month * 32 + value.day

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.YearlessDateField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

class YearlessDateRangeField(models.Field):
    def to_python(self, value):
        if isinstance(value, YearlessDateRange):
            return value
        if not value:
            return None
        start = int(value / 512)
        end = int(value % 512)
        start_date = YearlessDate(int(start / 32), start % 32)
        end_date = YearlessDate(int(end / 32), end % 32)
        return YearlessDateRange(start_date, end_date)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def db_type(self, connection):
        return 'mediumint'

    def get_prep_value(self, value):
        if value is not None:
            if isinstance(value, YearlessDateRange):
                start = value.start.month * 32 + value.start.day
                end = value.end.month * 32 + value.end.day
                return start * 512 + end
            elif isinstance(value, int): return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.YearlessDateRangeField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
