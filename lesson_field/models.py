from django.db import models

from .helpers import Lesson
from . import forms
from .settings import SHORT_WEEK_CHOICES, SHORT_DAY_CHOICES, LESSON_CHOICES

class LessonField(models.Field):
    week_choices = SHORT_WEEK_CHOICES
    day_choices = SHORT_DAY_CHOICES
    lesson_choices = LESSON_CHOICES

    def to_python(self, value):
        if isinstance(value, Lesson):
            return value
        if not value:
            return None
        return Lesson(value)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def db_type(self, connection):
        return 'smallint'

    def get_prep_value(self, value):
        if value is not None:
            if isinstance(value, Lesson):
                return value.value
            elif isinstance(value, int): return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.LessonField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
