import calendar
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

TEST_YEAR = 2008

@deconstructible
class YearlessDate(object):
    def __init__(self, month, day):
        self.month = int(month)
        self.day = int(day)
        self._validate()

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
        if not isinstance(other, YearlessDate): return False
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
