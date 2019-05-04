import calendar
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .settings import *

@deconstructible
class YearlessDate(object):
    def __init__(self, month, day, *args, **kwargs):
        super(YearlessDate, self).__init__(*args, **kwargs)
        self.month = int(month)
        self.day = int(day)
        self._validate()

    def create_range(self, end_date):
        return YearlessDateRange(self, end_date)

    def _validate(self):
        try:
            week, month_days = calendar.monthrange(TEST_YEAR, self.month)
        except calendar.IllegalMonthError:
            error = _("Cannot create YearlessDate object with a month value of {}.")
            raise ValueError(error.format(self.month))

        if self.day < 1 or self.day > month_days:
            error = _("Cannot create YearlessDate object - invalid day value {} for month {}.")
            raise ValueError(error.format(self.day, self.month_name))

    @property
    def month_name(self):
        return _(calendar.month_name[self.month])

    def __str__(self):
        return '{} {}'.format(self.day, self.month_name)

    def __eq__(self, other):
        return (self.day == other.day) and (self.month == other.month)

    def __gt__(self, other):
        if self.month != other.month:
            return self.month > other.month
        return self.day > other.day

    def __ne__(self, other):
        return not self == other

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return (self > other) or self == other

    def __lt__(self, other):
        return not self >= other

@deconstructible
class YearlessDateRange(object):
    def __init__(self, start, end, *args, **kwargs):
        super(YearlessDateRange, self).__init__(*args, **kwargs)
        self.start = start
        self.end = end
        self._validate()

    def _validate(self):
        sdi = isinstance(self.start, YearlessDate)
        edi = isinstance(self.end, YearlessDate)
        if not sdi or not edi:
            error = _("Start date and end date must be YearlessDate type.")
            raise ValueError(error.format(self.month))

    def are_overlap(self, other):
        array = list(enumerate([
            self.start, self.end,
            other.start, other.end
        ]))
        array.sort(key=lambda i: i[1])
        i = next(k for k, v in enumerate(array) if v[0] == 0)
        array = array[i:] + array[:i]
        return not all(x < y for x, y in zip(array, array[1:]))
