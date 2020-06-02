from django.conf import settings
from django.utils.translation import ugettext_lazy as _

WORK_DAYS = getattr(settings, 'LESSON_FIELD_WORK_DAYS', [0, 1, 2, 3, 4, 5])
MAX_LESSONS_DAY = getattr(settings, 'LESSON_FIELD_MAX_LESSONS_DAY', 5)
LESSONS_RANGE = range(1, MAX_LESSONS_DAY + 1)

WEEK_NAMES = (_('----'), _('numerator'), _('denominator'), _('both'))
SHORT_WEEK_NAMES = (_('----'), _('num'), _('denom'), _('both'))
DAY_NAMES = (
    _('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'), _('Friday'),
    _('Saturday'), _('Sunday'),
)
SHORT_DAY_NAMES = (
    _('mon'), _('tue'), _('wed'), _('thu'), _('fri'),
    _('sat'), _('sun'),
)

WEEK_CHOICES = [(k if k else '', v) for k, v in enumerate(WEEK_NAMES)]
SHORT_WEEK_CHOICES = [('', '----')] + [(k, v) for k, v in enumerate(SHORT_WEEK_NAMES)]
DAY_CHOICES = [('', '----')] + [(i, DAY_NAMES[i]) for i in WORK_DAYS]
SHORT_DAY_CHOICES = [('', '----')] + [(i, SHORT_DAY_NAMES[i]) for i in WORK_DAYS]
LESSON_CHOICES = [('', '----')] + [(i, i) for i in range(1, MAX_LESSONS_DAY + 1)]
