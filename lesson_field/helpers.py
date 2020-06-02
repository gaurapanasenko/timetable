from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy

from lesson_field import settings


@deconstructible
class Lesson:
    settings = settings

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

    def __getitem__(self, i):
        return [self.week, self.day, self.lesson][i]

    def __hash__(self):
        return hash(self.value)

    def __proxy__(self):
        return format_lazy(
            '{} - {} - {}', settings.SHORT_WEEK_NAMES[self.week],
            settings.SHORT_DAY_NAMES[self.day],
            format_lazy('{lesson} {name}', lesson=self.lesson, name=_('lesson'))
        )

    def __str__(self):
        return str(self.__proxy__())

    def __eq__(self, other):
        if isinstance(other, Lesson):
            return self.value == other.value
        return self.value == other

    def __gt__(self, other):
        if isinstance(other, Lesson):
            return self.value > other.value
        return self.value > other

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return (self > other) or self == other

    def __lt__(self, other):
        return not self >= other
