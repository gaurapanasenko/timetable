from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy

from .settings import *

@deconstructible
class Lesson(object):
    def __init__(self, value, *args, **kwargs):
        super(Lesson, self).__init__(*args, **kwargs)
        if isinstance(value, tuple):
            self.week = value[0]
            self.day = value[1]
            self.lesson = value[2]
        else:
            self.week = int(value / 256)
            self.day = int(value % 256 / 32)
            self.lesson = int(value % 32)

    @property
    def value(self):
        return self.week * 256 + self.day * 32 + self.lesson

    def __getitem__(self, x):
        return [self.week, self.day, self.lesson][x]

    def __hash__(self):
        return hash(self.value)

    def __proxy__(self):
        n = _('lesson')
        w = WEEK_NAMES[self.week]
        d = DAY_NAMES[self.day]
        ln = format_lazy('{lesson} {name}', lesson=self.lesson, name=n)
        return format_lazy('{} - {} - {}', w, d, ln)

    def __str__(self):
        return str(self.__proxy__())

    def __eq__(self, other):
        if isinstance(other, Lesson):
            return (self.value == other.value)
        else:
            return (self.value == other)

    def __gt__(self, other):
        if isinstance(other, Lesson):
            return (self.value > other.value)
        else:
            return (self.value > other)

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return (self > other) or self == other

    def __lt__(self, other):
        return not self >= other
