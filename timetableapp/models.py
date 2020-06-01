from datetime import date

from django.db import models
# from django.db.models import Max
from django.db.models.query import Q
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from yearlessdate.models import YearlessDateRangeField
from django_improvements.models import ReadOnlyOnExistForeignKey
# from lesson_field.helpers import Lesson
from lesson_field.models import LessonField
# from lesson_field.settings import WEEK_CHOICES, DAY_CHOICES, LESSON_CHOICES

from timetableapp.settings import current_year, START_YEAR


def year_min_value(value):
    """Create dynamic validator for minimal year value."""
    return MinValueValidator(START_YEAR)(value)


def year_max_value(value):
    """Create dynamic validator for maximal year value."""
    return MaxValueValidator(current_year())(value)


class Faculty(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=128,
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_('abbreviation'),
        max_length=16,
        default=None,
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self, test=None):
        abbreviation = self.abbreviation
        return abbreviation if abbreviation else self.name

    class Meta:
        verbose_name = _('Faculty object')
        verbose_name_plural = _('faculties')
        ordering = ['abbreviation', 'name']


class Department(models.Model):
    faculty = models.ForeignKey(
        'Faculty',
        on_delete=models.PROTECT,
        verbose_name=_('faculty'),
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=128,
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_('abbreviation'),
        max_length=16,
        default=None,
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        abbreviation = self.abbreviation
        return abbreviation if abbreviation else self.name

    class Meta:
        verbose_name = _('Department object')
        verbose_name_plural = _('departments')
        ordering = ['abbreviation', 'name']


class Subject(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=128,
        unique=True,
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
        verbose_name=_('department'),
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return '%s - %s' % (self.name, self.department)

    class Meta:
        verbose_name = _('Subject object')
        verbose_name_plural = _('subjects')
        unique_together = [['name', 'department']]
        ordering = ['name', 'department']


class Person(models.Model):
    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=128,
    )

    middle_name = models.CharField(
        verbose_name=_('middle name'),
        max_length=128,
    )

    last_name = models.CharField(
        verbose_name=_('last name'),
        max_length=128,
    )

    def __str__(self):
        args = (self.first_name, self.middle_name, self.last_name)
        return '%s %s %s' % args

    class Meta:
        verbose_name = _('Person object')
        verbose_name_plural = _('persons')
        unique_together = [['first_name', 'middle_name', 'last_name']]
        ordering = ['first_name', 'middle_name', 'last_name']


class Teacher(models.Model):
    person = models.OneToOneField(
        'Person',
        on_delete=models.PROTECT,
        verbose_name=_('person'),
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
        verbose_name=_('department'),
    )
    # work_time = models.BigIntegerField(
    #     verbose_name=_('work time'),
    #     default=2**60,
    #     validators=[MinValueValidator(0), MaxValueValidator(2**60)]
    # )

    def __str__(self):
        return '%s' % self.person

    class Meta:
        verbose_name = _('Teacher object')
        verbose_name_plural = _('teachers')
        ordering = ['person', ]


class Specialty(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=128,
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_('number'),
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_('abbreviation'),
        max_length=16,
        unique=True,
    )
    faculty = models.ForeignKey(
        'Faculty',
        on_delete=models.PROTECT,
        verbose_name=_('faculty'),
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return '%s - %s' % (self.number, self.name)

    class Meta:
        verbose_name = _('Specialty object')
        verbose_name_plural = _('specialties')
        ordering = ['abbreviation', ]


class Building(models.Model):
    number = models.PositiveSmallIntegerField(
        verbose_name=_('number'),
        unique=True,
    )
    address = models.CharField(
        verbose_name=_('address'),
        max_length=128,
        unique=True,
        default=None,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        verbose_name=_('longitude'),
        max_digits=9,
        decimal_places=6,
        default=None,
        blank=True,
        null=True,
    )
    latitude = models.DecimalField(
        verbose_name=_('latitude'),
        max_digits=9,
        decimal_places=6,
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = _('Building object')
        verbose_name_plural = _('buildings')
        ordering = ['number', ]


class Classroom(models.Model):
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        verbose_name=_('building'),
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_('number'),
    )

    def __str__(self):
        return '%s/%s' % (self.building.number, self.number)

    class Meta:
        verbose_name = _('Classroom object')
        verbose_name_plural = _('classrooms')
        unique_together = [['building', 'number']]
        ordering = ['building', 'number', ]


class FormOfStudy(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=128,
        unique=True,
    )
    suffix = models.CharField(
        verbose_name=_('suffix'),
        max_length=16,
        blank=True,
        unique=True,
    )
    semesters = models.PositiveSmallIntegerField(
        verbose_name=_('number of semesters'),
        help_text=_("Total number of semesters, later if you specify fewer Semester date ranges than Number of semesters they will cycle from beginning automatically."),
        default=8,
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('priority'),
        choices=((x, x) for x in range(1, 10)),
        default=5,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Form of study object')
        verbose_name_plural = _('forms of study')
        ordering = ['priority', 'suffix']


class FormOfStudySemester(models.Model):
    form = models.ForeignKey(
        'FormOfStudy',
        on_delete=models.PROTECT,
        verbose_name=_('form of study'),
        # default={'priority': 1},
    )
    date_range = YearlessDateRangeField(
        verbose_name=_('default date range'),
    )

    def __str__(self):
        return str(_("default date range for semester"))

    class Meta:
        verbose_name = _('Semester date range object')
        verbose_name_plural = _('semester date ranges')


class GroupStream(ReadOnlyOnExistForeignKey, models.Model):
    specialty = models.ForeignKey(
        'Specialty',
        on_delete=models.PROTECT,
        verbose_name=_('specialty'),
        db_index=True,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name=_('year'),
        default=current_year,
        validators=[year_min_value, year_max_value],
        db_index=True,
    )
    form = models.ForeignKey(
        'FormOfStudy',
        on_delete=models.PROTECT,
        verbose_name=_('form of study'),
        db_index=True,
        # default={'priority': 1},
    )

    readonly_fields = [
        (('Curriculum',), ('year', 'form_id'))
    ]

    def save(self, *args, **kwargs):
        form = None
        try:
            form = self.form
        except FormOfStudy.DoesNotExist:
            pass
        new = False
        if self.pk is None:
            new = True
        super(GroupStream, self).save(*args, **kwargs)
        if new and form:
            objs = FormOfStudySemester.objects.filter(form=form)
            if objs.exists():
                count = objs.count()
                year = self.year
                semesters = self.form.semesters
                last_date = date(year - 1, 1, 1)
                for i in range(1, semesters + 1):
                    date_range = objs[(i - 1) % count].date_range
                    std = date(year, date_range.start.month, date_range.start.day)
                    while std < last_date:
                        year += 1
                        std = date(year, date_range.start.month, date_range.start.day)
                    last_date = std
                    etd = date(year, date_range.end.month, date_range.end.day)
                    while etd < last_date:
                        year += 1
                        etd = date(year, date_range.end.month, date_range.end.day)
                    last_date = etd
                    args_dict = {
                        'group_stream': self,
                        'semester': i,
                        'start_date': std,
                        'end_date': etd,
                    }
                    Curriculum.objects.create(**args_dict)
        if not Group.objects.filter(group_stream=self).exists():
            Group.objects.create(group_stream=self)

    def get_union_group(self):
        group = self.group_set.filter(number=0).first()
        if not group:
            group = self.group_set.create()
        return group

    def get_conflict_groups(self, group):
        query = self.group_set.exclude(pk=group.pk)
        if not group.is_union():
            query = query.filter(number=0)
        return query

    def __str__(self):
        return '%s-%s%s' % (
            self.specialty.abbreviation,
            str(self.year % 100),
            self.form.suffix,
        )

    class Meta:
        verbose_name = _('Group stream object')
        verbose_name_plural = _('group streams')
        unique_together = [['specialty', 'year', 'form']]
        ordering = ['-year', 'specialty', 'form']


class Group(ReadOnlyOnExistForeignKey, models.Model):
    group_stream = models.ForeignKey(
        'GroupStream',
        on_delete=models.CASCADE,
        verbose_name=_('group stream'),
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_('number'),
        default=0,
        help_text=_("If is zero then it will be union of groups in group stream.")
    )

    readonly_fields = [
        (
            (
                'SubGroup',
                'CurriculumRecordingTimings',
            ),
            ('group_stream_id', 'number',)
        )
    ]

    def is_union(self):
        return self.number == 0

    def get_real(self):
        if self.is_union():
            return self.group_stream
        return self

    def get_conflict_subgroups(self, subgroup):
        group_stream = self.group_stream
        groups = group_stream.get_conflict_groups(self).values("pk")
        if subgroup.is_union():
            query = Q(group=self)
        else:
            query = Q(group=self) & Q(numerator=0) & Q(denominator=0)
        return SubGroup.objects.filter(Q(group__in=groups) | query)

    def get_union_subgroup(self):
        subgroup = self.subgroup_set.filter(numerator=0, denominator=0).first()
        if not subgroup:
            subgroup = self.subgroup_set.create()
        return subgroup

    def save(self, *args, **kwargs):
        super(Group, self).save(*args, **kwargs)
        if not SubGroup.objects.filter(group=self).exists():
            SubGroup.objects.create(group=self)

    def __str__(self):
        if self.number == 0:
            return str(self.group_stream)
        return '%s-%s' % (self.group_stream, self.number)

    class Meta:
        verbose_name = _('Group object')
        verbose_name_plural = _('groups')
        unique_together = (('group_stream', 'number'))


class SubGroup(ReadOnlyOnExistForeignKey, models.Model):
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_('group stream'),
    )
    numerator = models.PositiveSmallIntegerField(
        verbose_name=_('numerator'),
        default=0,
        help_text=_("Index of subgroup."),
    )
    denominator = models.PositiveSmallIntegerField(
        verbose_name=_('denominator'),
        default=0,
        help_text=_("Total number of subgroups in this type of subgroup."),
    )

    readonly_fields = [
        (
            ('Lesson',),
            ('group_id', 'numerator', 'denominator',)
        )
    ]

    def is_union(self):
        return self.numerator == 0 and self.denominator == 0

    def get_real(self):
        if self.is_union():
            return self.group.get_real()
        return self

    def get_conflict_subgroups(self):
        group = self.group
        query = group.get_conflict_subgroups(self)
        if self.is_union():
            return group.subgroup_set.all() + query
        return query

    def clean(self):
        if self.group.number == 0:
            if not self.is_union():
                error = _("Group is union of groups, so numerator and denominator must be zero.")
                raise ValidationError(error)
        elif self.numerator == 0 and self.denominator != 0:
            error = _("If group is not union of groups, numerator can not be zero.")
            raise ValidationError(error)
        if self.numerator > self.denominator:
            error = _("Numerator must be lower or equal to denominator.")
            raise ValidationError(error)
        super().clean()

    def __str__(self):
        if self.numerator == 0:
            return str(self.group)
        return '%s-%s/%s' % (self.group, self.numerator, self.denominator)

    class Meta:
        verbose_name = _('Subgroup object')
        verbose_name_plural = _('subgroups')
        unique_together = (('group', 'numerator', 'denominator'))


class Curriculum(models.Model):
    group_stream = models.ForeignKey(
        'GroupStream',
        on_delete=models.CASCADE,
        verbose_name=_('group stream'),
    )
    semester = models.PositiveSmallIntegerField(
        verbose_name=_('semester'),
    )

    start_date = models.DateField(
        verbose_name=_('start date'),
        default=None,
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        verbose_name=_('end date'),
        default=None,
        blank=True,
        null=True,
    )

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            error = _("End date should be greater than start date.")
            raise ValidationError(error)
        super(Curriculum, self).clean()

    def __str__(self):
        semester = format_lazy(
            '{semester} {name}', semester=self.semester, name=_('semester'))
        return '%s - %s' % (self.group_stream, semester)

    class Meta:
        verbose_name = _('Curriculum object')
        verbose_name_plural = _('curriculums')
        unique_together = (('group_stream', 'semester'))
        ordering = ('group_stream', 'semester',)


class CurriculumRecordingTimings(models.Model):
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_('group'),
    )
    semester = models.PositiveSmallIntegerField(
        verbose_name=_('semester'),
    )
    subjects = models.ManyToManyField(
        'Subject',
        verbose_name=_('subjects'),
    )
    lectures = models.PositiveSmallIntegerField(
        verbose_name=_('number of lectures'),
    )
    practices = models.PositiveSmallIntegerField(
        verbose_name=_('number of practices'),
    )
    laboratory = models.PositiveSmallIntegerField(
        verbose_name=_('number of laboratory'),
    )
    independent_work = models.PositiveSmallIntegerField(
        verbose_name=_('amount of independent work'),
    )

    def get_subject_name(self):
        return '/'.join(str(i.name) for i in self.subjects.all())

    def __str__(self):
        subjects = self.get_subject_name()
        if subjects:
            subjects = ' - ' + subjects
        semester = format_lazy(
            '{semester} {name}', semester=self.semester, name=_('semester'))
        return '%s - %s%s' % (self.group, semester, subjects)

    class Meta:
        verbose_name = _('Curriculum record object')
        verbose_name_plural = _('curriculum records')
        ordering = ['group', 'semester']


class Lesson(ReadOnlyOnExistForeignKey, models.Model):
    LESSON_CHOICES = [
        (0, 'Lectures'),
        (1, 'Practices'),
        (2, 'Laboratory'),
    ]

    subgroup = models.ForeignKey(
        'SubGroup',
        on_delete=models.CASCADE,
        verbose_name=_('subgroup'),
    )

    semester = models.PositiveSmallIntegerField(
        verbose_name=_('semester'),
    )

    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        verbose_name=_('subjects'),
    )

    lesson = models.PositiveSmallIntegerField(
        verbose_name=_('lesson'),
        choices=LESSON_CHOICES,
        default=0,
    )

    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        verbose_name=_('teacher'),
        default=None,
        blank=True,
        null=True,
    )

    readonly_fields = [
        (
            ('TimeTableRecording',),
            ('subgroup_id',)
        )
    ]

    def get_conflicting(self):
        subgroup = self.subgroup
        conflict = subgroup.get_conflict_subgroups()
        pks = conflict.values("pk")
        return Lesson.objects.exclude(pk=self.pk).filter(
            subgroup__in=pks,
            semester=self.semester,
            subject=self.subject,
            lesson=self.lesson,
        )

    def validate_unique(self, exclude=None):
        confliting = self.get_conflicting()
        filt = confliting.filter(teacher=self.teacher)
        if filt.exclude(pk=self.pk).exists():
            error = _("Duplicate teacher for lesson by {}.")
            raise ValidationError(error.format(filt.first()))
        super().validate_unique(exclude)

    def __str__(self):
        semester = format_lazy(
            '{semester} {name}', semester=self.semester, name=_('semester'))
        return '%s - %s - %s - %s' % (
            self.subgroup, semester, self.subject,
            dict(self.LESSON_CHOICES)[self.lesson],
        )

    class Meta:
        verbose_name = _('Lesson object')
        verbose_name_plural = _('lessons')
        unique_together = ((
            'subgroup', 'semester', 'subject', 'lesson',
        ),)


class TimeTableRecording(models.Model):
    lesson = models.ForeignKey(
        'Lesson',
        on_delete=models.CASCADE,
        verbose_name=_('lesson'),
    )

    lesson_number = LessonField(
        verbose_name=_('lesson number'),
    )

    classroom = models.ForeignKey(
        'Classroom',
        on_delete=models.CASCADE,
        verbose_name=_('classroom'),
        default=None,
        null=True,
        blank=True,
    )

    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        verbose_name=_('teacher'),
        default=None,
        null=True,
        blank=True,
    )

    start_date = models.DateField(
        verbose_name=_('start date'),
        default=None,
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        verbose_name=_('end date'),
        default=None,
        blank=True,
        null=True,
    )

    def validate_unique(self, exclude=None):
        confliting = self.lesson.get_conflicting().values('pk')
        filt = TimeTableRecording.objects.filter(lesson__in=confliting)
        if filt.exclude(pk=self.pk).exists():
            error = _("Duplicate time table recording by {}.")
            raise ValidationError(error.format(filt.first()))
        super().validate_unique(exclude)

    def __str__(self):
        return '%s - %s' % (self.lesson, self.lesson_number)

    class Meta:
        verbose_name = _('Timetable recording object')
        verbose_name_plural = _('timetable recordings')
        unique_together = (('lesson', 'lesson_number'),)
