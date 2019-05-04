from datetime import date

from django.db import models
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from mptt.models import MPTTModel, TreeForeignKey

from yearlessdate.models import YearlessDateField, YearlessDateRangeField
from django_improvements.models import ReadOnlyOnExistForeignKey

from .settings import *

def year_min_value(value):
    return MinValueValidator(START_YEAR)(value)

def year_max_value(value):
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

    def __str__(self):
        return self.abbreviation if self.abbreviation else self.name

    class Meta:
        verbose_name = _('faculty')
        verbose_name_plural = _('faculties')

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
        return self.abbreviation if self.abbreviation else self.name

    class Meta:
        verbose_name = _('department')
        verbose_name_plural = _('departments')

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
        return self.name

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')

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
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        unique_together = [['first_name', 'middle_name', 'last_name']]

class Teacher(models.Model):
    person = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        verbose_name=_('person'),
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
        verbose_name=_('department'),
        default=None,
        null=True,
        blank=True,
    )
    #~ work_time = models.BigIntegerField(
        #~ verbose_name=_('work time'),
        #~ default=2**60,
        #~ validators=[MinValueValidator(0), MaxValueValidator(2**60)]
    #~ )

    def __str__(self):
        return '%s' % self.person

    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

class Specialty(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=128,
        unique=True,
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
        return "%s - %s" % (self.number, self.name)

    class Meta:
        verbose_name = _('specialty')
        verbose_name_plural = _('specialties')

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
        b = self.number
        n = Building._meta.verbose_name
        return str(format_lazy('{building} {name}', building=b, name=n))

    class Meta:
        verbose_name = _('building')
        verbose_name_plural = _('buildings')


class Classroom(models.Model):
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        verbose_name=_('building'),
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_('number'),
        unique=True,
    )

    def __str__(self):
        return '%s/%s' % (self.building.number, self.number)

    class Meta:
        verbose_name = _('classroom')
        verbose_name_plural = _('classrooms')

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
        choices=((x, x) for x in range(1,10)),
        default=5,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('form of study')
        verbose_name_plural = _('forms of study')
        ordering = ['priority']

class FormOfStudySemester(models.Model):
    form = models.ForeignKey(
        'FormOfStudy',
        on_delete=models.PROTECT,
        verbose_name=_('form of study'),
        #~ default={'priority': 1},
    )
    date_range = YearlessDateRangeField(
        verbose_name=_('default date range'),
    )

    def __str__(self):
        return str(_("default date range for semester"))

    class Meta:
        verbose_name = _('semester date range')
        verbose_name_plural = _('semester date ranges')

class GroupStream(ReadOnlyOnExistForeignKey, models.Model):
    specialty = models.ForeignKey(
        'Specialty',
        on_delete=models.PROTECT,
        verbose_name=_('specialty'),
    )
    year = models.PositiveSmallIntegerField(
        verbose_name=_('year'),
        default=current_year,
        validators=[year_min_value, year_max_value],
    )
    form = models.ForeignKey(
        'FormOfStudy',
        on_delete=models.PROTECT,
        verbose_name=_('form of study'),
        #~ default={'priority': 1},
    )

    important_fields = ['year', 'form']
    related_models = [('timetableapp', 'GroupStreamSemester', 'group')]

    def save(self, *args, **kwargs):
        form = None
        try: form = self.form
        except FormOfStudy.DoesNotExist as e: pass
        new = False
        if self.pk is None: new = True
        super(GroupStream, self).save(*args, **kwargs)
        if new and form:
            objs = FormOfStudySemester.objects.filter(form=form)
            if objs.exists():
                pass
                count = objs.count()
                year = self.year
                semesters = self.form.semesters
                last_date = date(year - 1, 1, 1)
                for i in range(1, semesters + 1):
                    dr = objs[(i - 1) % count].date_range
                    std = date(year, dr.start.month, dr.start.day)
                    while std < last_date:
                        year += 1
                        std = date(year, dr.start.month, dr.start.day)
                    last_date = std
                    etd = date(year, dr.end.month, dr.end.day)
                    while etd < last_date:
                        year += 1
                        etd = date(year, dr.end.month, dr.end.day)
                    last_date = etd
                    args_dict = {
                        'group': self,
                        'semester': i,
                        'start_date': std,
                        'end_date': etd,
                    }
                    GroupStreamSemester.objects.create(**args_dict)
        if not Group.objects.filter(group_stream=self).exists():
            Group.objects.create(group_stream=self)

    def __str__(self):
        return '%s-%s%s' % (
            self.specialty.abbreviation,
            str(self.year % 100),
            self.form.suffix,
        )

    class Meta:
        verbose_name = _('group stream')
        verbose_name_plural = _('group streams')
        unique_together = [['specialty', 'year', 'form']]

class GroupStreamSemester(models.Model):
    group = models.ForeignKey(
        'GroupStream',
        on_delete=models.CASCADE,
        verbose_name=_('group stream'),
    )

    semester = models.PositiveSmallIntegerField(
        verbose_name=_('semester'),
        validators=[MinValueValidator(1)],
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
        super(GroupStreamSemester, self).clean()

    def __str__(self):
        s = self.semester
        n = _('semester')
        semester = format_lazy('{semester} {name}', semester=s, name=n)
        return '{} - {}'.format(self.group, semester)

    class Meta:
        verbose_name = _('group stream semester')
        verbose_name_plural = _('group stream semesters')
        unique_together = [['group', 'semester']]

class Group(ReadOnlyOnExistForeignKey, MPTTModel):
    def generate_number_choices():
        l = [(None,'-')]
        for x in range(1, 9):
            l.append((x, x))
        return l

    NUMBER_CHOICES = generate_number_choices()

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name=_('parent node'),
        default=None,
        blank=True,
        null=True,
    )
    group_stream = models.ForeignKey(
        'GroupStream',
        on_delete=models.CASCADE,
        verbose_name=_('group stream'),
        help_text=_('If Parent node is set, this field fills automatically while saving.'),
        default=None,
        blank=True,
        null=True,
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_('number'),
        choices=NUMBER_CHOICES,
        default=None,
        blank=True,
        null=True,
    )

    important_fields = ['parent']
    related_models = [
        ('timetableapp', 'CurriculumRecord', 'group'),
        ('timetableapp', 'CurriculumRecordTeacher', 'group'),
    ]

    def save(self, *args, **kwargs):
        parent = None
        try: parent = self.parent
        except Group.DoesNotExist as e: pass
        if self.parent is not None:
            self.group_stream = self.parent.group_stream
        elif self.number is not None:
            self.number = None
        super(Group, self).save(*args, **kwargs)

    def clean(self):
        if self.parent is not None:
            if self == self.parent:
                error = _("Group can't be child of itself.")
                raise ValidationError(error)
            if self.number is None:
                error = _("Number may not be empty when Parent node is set.")
                raise ValidationError(error)
            depth = self.calculate_max_depth_of_childs()
            if depth > MAX_GROUP_TREE_HEIGHT:
                error = _("Group can't have parent node with such depth.")
                raise ValidationError(error)
        super(Group, self).clean()

    def get_path_to_root(self):
        arr = []
        p = self.parent
        while p is not None:
            arr.append(p)
            p = p.parent
        return arr

    def get_childs(self):
        arr = []
        childs = Group.objects.filter(parent=self, parent__isnull=False)
        arr += childs
        for i in childs:
            arr += i.get_childs()
        return arr

    def get_path_to_root_and_childs(self):
        return [self] + self.get_path_to_root() + self.get_childs()

    def is_child(self, parent):
        p = self.parent
        while p is not None:
            if p == parent:
                return True
            p = p.parent
        return False

    def calculate_node_height(self, depth=0):
        childs = Group.objects.filter(parent=self, parent__isnull=False)
        max_depth = depth
        for i in childs:
            m = i.calculate_node_height(depth + 1)
            if max_depth < m: max_depth = m
        return max_depth

    def calculate_max_depth_of_childs(self):
        return 1 + len(self.get_path_to_root()) + self.calculate_node_height()

    def __str__(self):
        number = [self] + self.get_path_to_root()
        args = (
            str(self.group_stream),
            ''.join('-%s' % i.number for i in reversed(number[:-1])),
        )
        return '%s%s' % args

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        unique_together = [['parent', 'number']]

    class MPTTMeta:
        order_insertion_by = ['number']

class Curriculum(models.Model):
    group = models.ForeignKey(
        'GroupStream',
        on_delete=models.CASCADE,
        verbose_name=_('group stream'),
    )
    semester = models.PositiveSmallIntegerField(
        verbose_name=_('semester'),
    )

    def __str__(self):
        s = self.semester
        n = _('semester')
        semester = format_lazy('{semester} {name}', semester=s, name=n)
        return '%s - %s' % (self.group, semester)

    class Meta:
        verbose_name = _('curriculum')
        verbose_name_plural = _('curriculums')
        unique_together = [['group', 'semester']]


class CurriculumRecord(models.Model):
    curriculum = models.ForeignKey(
        'Curriculum',
        on_delete=models.CASCADE,
        verbose_name=_('curriculum'),
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_('group'),
    )
    subjects = models.ManyToManyField(
        Subject,
        through='CurriculumRecordSubject',
        verbose_name=_('subjects'),
    )
    teachers = models.ManyToManyField(
        Teacher,
        through='CurriculumRecordTeacher',
        verbose_name=_('teachers'),
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

    def clean(self):
        curriculum = None
        group = None
        try: curriculum = self.curriculum
        except Curriculum.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if curriculum and group and group.group_stream != curriculum.group:
            error = _("Group must be child of or same as group in curriculum.")
            raise ValidationError(error)
        super(CurriculumRecord, self).clean()

    def get_semester(self):
        return self.curriculum.semester

    def get_subject_name(self):
        return '/'.join(str(i) for i in self.subjects.all())

    def __str__(self):
        subjects = self.get_subject_name()
        if subjects: subjects = ' - ' + subjects
        s = self.get_semester()
        n = _('semester')
        semester = format_lazy('{semester} {name}', semester=s, name=n)
        return '%s - %s%s' % (self.group, semester, subjects)

    class Meta:
        verbose_name = _('curriculum record')
        verbose_name_plural = _('curriculum records')

class CurriculumRecordSubject(models.Model):
    record = models.ForeignKey(
        'CurriculumRecord',
        on_delete=models.CASCADE,
        verbose_name=_('curriculum record'),
    )

    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        verbose_name=_('subject'),
    )

    def get_group(self):
        return self.record.group

    def get_semester(self):
        return self.record.get_semester()

    def __str__(self):
        s = self.get_semester()
        n = _('semester')
        semester = format_lazy('{semester} {name}', semester=s, name=n)
        return '%s - %s - %s' % (self.get_group(), semester, self.subject)

    class Meta:
        verbose_name = _('subject for curriculum record')
        verbose_name_plural = _('subjects for curriculum records')

class CurriculumRecordTeacher(models.Model):
    RESPONSIBILITY_CHOICES = [
        (0, 'Lectures'),
        (1, 'Practices'),
        (2, 'Laboratory'),
    ]

    record = models.ForeignKey(
        'CurriculumRecord',
        on_delete=models.CASCADE,
        verbose_name=_('curriculum record'),
    )

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_('group'),
    )

    responsibility = models.PositiveSmallIntegerField(
        verbose_name=_('responsibility'),
        choices=RESPONSIBILITY_CHOICES,
        default=0,
    )

    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        verbose_name=_('teacher'),
    )

    def clean(self):
        record = None
        group = None
        try: record = self.record
        except CurriculumRecord.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if record and group:
            pg = record.group
            if pg != group and not group.is_child(pg):
                error = _("Group must be child of or same as group in record")
                raise ValidationError(error)
        super(CurriculumRecordTeacher, self).clean()

    def validate_unique(self, exclude=None):
        record = None
        group = None
        try: record = self.record
        except CurriculumRecord.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if record and group:
            arr = group.get_path_to_root_and_childs() if group else []
            args = {
                'record': record,
                'group__in': arr,
                'responsibility': self.responsibility,
            }
            f = CurriculumRecordTeacher.objects.exclude(id=self.id).filter(**args)
            if f.exists():
                error = _("Duplicate teacher for curriculum record through group {}.")
                raise ValidationError(error.format(f.first().group))
        super(CurriculumRecordTeacher, self).validate_unique(exclude)

    def __str__(self):
        rc = dict(self.RESPONSIBILITY_CHOICES)
        responsibility = rc[self.responsibility]
        args = (self.group, responsibility, self.teacher)
        return '%s - %s - %s' % args

    class Meta:
        verbose_name = _('teacher for curriculum record')
        verbose_name_plural = _('teachers for curriculum records')
        unique_together = [[
            'record', 'group', 'responsibility',
        ]]


class TimetableRecording(models.Model):
    def generate_lesson_choices():
        arr = []
        weeks = (_('numerator'), _('denominator'))
        days = (
            _('mon'), _('tue'), _('wed'), _('thu'), _('fri'),
            _('sat'), _('sun')
        )
        n = _('lesson')
        for ik, iv in enumerate(weeks):
            for j in WORK_DAYS:
                for k in range(1, MAX_LESSONS_DAY + 1):
                    l = format_lazy('{lesson} {name}', lesson=k, name=n)
                    val = ik * 256 + j * 32 + k
                    arr.append((val, '%s - %s - %s' % (iv, days[j], l)))
        return arr

    LESSON_CHOICES = generate_lesson_choices()

    record = models.ForeignKey(
        'CurriculumRecord',
        on_delete=models.CASCADE,
        verbose_name=_('curriculum record'),
    )

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_('group'),
    )

    lesson = models.PositiveSmallIntegerField(
        verbose_name=_('lesson number'),
        choices=LESSON_CHOICES,
        default=0,
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

    def clean(self):
        record = None
        group = None
        try: record = self.record
        except CurriculumRecord.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if record and group:
            pg = record.group
            if pg != group and not group.is_child(pg):
                error = _("Group must be child of or same as group in curriculum record")
                raise ValidationError(error)
        super(TimetableRecord, self).clean()

    def validate_unique(self, exclude=None):
        record = None
        group = None
        try: record = self.record
        except CurriculumRecord.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if group:
            arr = group.get_path_to_root_and_childs()
            args = {
                'record': record,
                'group__in': arr,
                'lesson': self.lesson,
            }
            f = TimetableRecord.objects.exclude(id=self.id).filter(**args)
            if f.exists():
                error = _("Duplicate timetable record trough group {}.")
                raise ValidationError(error.format(f.first().group))
        super(TimetableRecord, self).validate_unique(exclude)

    def __str__(self):
        s = self.record.getSemester()
        n = _('semester')
        semester = format_lazy('{semester} {name}', semester=s, name=n)
        lesson = dict(self.LESSON_CHOICES)[self.lesson]
        args = (str(self.group), semester, lesson, self.record.getSubjectName())
        return '%s - %s - %s - %s' % args

    class Meta:
        verbose_name = _('timetable recording')
        verbose_name_plural = _('timetable recordings')
        unique_together = [
            ['record', 'group', 'lesson'], ['lesson', 'classroom']
        ]
