from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.admin import widgets
from django.apps import apps
from django import forms

from yearlessdate.models import YearlessDateField

from .settings import *

def year_max_value(value):
    return MaxValueValidator(current_year())(value)

class ReadOnlyOnExistForeignKey(object):
    def __init__(self, *args, **kwargs):
        super(ReadOnlyOnExistForeignKey, self).__init__(*args, **kwargs)
        self.__important_fields = getattr(self, 'important_fields')
        self.__related_models = getattr(self, 'related_models')
        for field in self.__important_fields:
            try:
                setattr(self, '__original_%s' % field, getattr(self, field))
            except:
                setattr(self, '__original_%s' % field, None)

    def has_changed(self):
        for field in self.__important_fields:
            orig = '__original_%s' % field
            new_value = None
            try: new_value = getattr(self, field)
            except: pass
            if getattr(self, orig) != new_value:
                return True
        return False

    def clean(self, *args, **kwargs):
        models = []
        for i in self.__related_models:
            models.append((apps.get_model('timetableapp', i[0]), i[1]))
        fields = self.__important_fields
        exists = False
        for i in models:
            if i[0].objects.filter(**{i[1]: self}).exists():
                exists = True
                break
        if exists and self.has_changed():
            error = _("{} fields can't be changed when {} exists")
            flds = [str(self._meta.get_field(i).verbose_name) for i in fields]
            f = _(" and ").join(flds)
            mdls = [str(i[0]._meta.verbose_name) for i in models]
            m = _(" and ").join(mdls)
            raise ValidationError(error.format(f, m))
        super(ReadOnlyOnExistForeignKey, self).clean(*args, **kwargs)


class Faculty(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=128,
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_('Abbreviation'),
        max_length=16,
        default=None,
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.abbreviation if self.abbreviation else self.name

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

class Department(models.Model):
    faculty = models.ForeignKey(
        'Faculty',
        on_delete=models.PROTECT,
        verbose_name=_('Faculty'),
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=128,
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_('Abbreviation'),
        max_length=16,
        default=None,
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.abbreviation if self.abbreviation else self.name

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

class Subject(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=128,
        unique=True,
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
        verbose_name=_('Department'),
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

class Person(models.Model):
    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=128,
    )

    middle_name = models.CharField(
        verbose_name=_('Middle name'),
        max_length=128,
    )

    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=128,
    )

    def __str__(self):
        args = (self.first_name, self.middle_name, self.last_name)
        return '%s %s %s' % args

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        unique_together = [['first_name', 'middle_name', 'last_name']]

class Teacher(models.Model):
    person = models.ForeignKey(
        'Person',
        on_delete=models.PROTECT,
        verbose_name=_('Person'),
    )
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
        verbose_name=_('Department'),
        default=None,
        null=True,
        blank=True,
    )
    #~ work_time = models.BigIntegerField(
        #~ verbose_name=_('Work time'),
        #~ default=2**60,
        #~ validators=[MinValueValidator(0), MaxValueValidator(2**60)]
    #~ )

    def __str__(self):
        return '%s' % self.person

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

class Specialty(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=128,
        unique=True,
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_('Number'),
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_('Abbreviation'),
        max_length=16,
        unique=True,
    )
    faculty = models.ForeignKey(
        'Faculty',
        on_delete=models.PROTECT,
        verbose_name=_('Faculty'),
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "%s - %s" % (self.number, self.name)

    class Meta:
        verbose_name = _('Specialty')
        verbose_name_plural = _('Specialties')

class Building(models.Model):
    number = models.PositiveSmallIntegerField(
        verbose_name=_('Number'),
        unique=True,
    )
    address = models.CharField(
        verbose_name=_('Address'),
        max_length=128,
        unique=True,
        default=None,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        verbose_name=_('Longitude'),
        max_digits=9,
        decimal_places=6,
        default=None,
        blank=True,
        null=True,
    )
    latitude = models.DecimalField(
        verbose_name=_('Longitude'),
        max_digits=9,
        decimal_places=6,
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self):
        return _('{building} building').format(building=self.number)

    class Meta:
        verbose_name = _('Building')
        verbose_name_plural = _('Buildings')


class Classroom(models.Model):
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        verbose_name=_('Building'),
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_('Number'),
        unique=True,
    )

    def __str__(self):
        return '%s/%s' % (self.building.number, self.number)

    class Meta:
        verbose_name = _('Classroom')
        verbose_name_plural = _('Classrooms')

class FormOfStudy(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=128,
        unique=True,
    )
    suffix = models.CharField(
        verbose_name=_('Suffix'),
        max_length=16,
        blank=True,
        unique=True,
    )
    semesters = models.PositiveSmallIntegerField(
        verbose_name=_('Number of semesters'),
        default=8,
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name=_('Priority'),
        choices=((x, x) for x in range(1,10)),
        default=5,
    )
    start_date_first = YearlessDateField(
        verbose_name=_('Default start date for first semester'),
        default=None,
        blank=True,
        null=True,
    )
    end_date_first = YearlessDateField(
        verbose_name=_('Default end date for first semester'),
        default=None,
        blank=True,
        null=True,
    )
    start_date_second = YearlessDateField(
        verbose_name=_('Default start date for second semester'),
        default=None,
        blank=True,
        null=True,
    )
    end_date_second = YearlessDateField(
        verbose_name=_('Default end date for second semester'),
        default=None,
        blank=True,
        null=True,
    )

    def clean(self):
        r1 = self.start_date_first.create_range(self.end_date_first)
        r2 = self.start_date_second.create_range(self.end_date_second)
        if r1.is_intersecting(r2):
            error = _("Date ranges are intersecting")
            raise ValidationError(error)
        super(FormOfStudy, self).clean()


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Form of study')
        verbose_name_plural = _('Forms of study')
        ordering = ['priority']

class GroupStream(ReadOnlyOnExistForeignKey, models.Model):
    specialty = models.ForeignKey(
        'Specialty',
        on_delete=models.PROTECT,
        verbose_name=_('Specialty'),
    )
    year = models.PositiveSmallIntegerField(
        verbose_name=_('Year'),
        default=current_year,
        validators=[MinValueValidator(START_YEAR), year_max_value],
    )
    form = models.ForeignKey(
        'FormOfStudy',
        on_delete=models.PROTECT,
        verbose_name=_('Form of study'),
        default={'priority': 1},
    )

    important_fields = ['year', 'form']
    related_models = [('SemesterSchedule', 'group')]

    def save(self, *args, **kwargs):
        new = False
        if self.pk is None: new = True
        super(GroupStream, self).save(*args, **kwargs)
        if new:
            st1 = self.form.start_date_first
            et1 = self.form.end_date_first
            st2 = self.form.start_date_second
            et2 = self.form.end_date_second
            if st1 and et1 and st2 and et2:
                semesters = self.form.semesters
                for i in range(1, semesters + 1):
                    y = int(self.year + i / 2)
                    std = st1 if i % 2 else st2
                    std = datetime.date(y, std.month, std.day)
                    etd = et1 if i % 2 else et2
                    etd = datetime.date(y, etd.month, etd.day)
                    if etd < std:
                        etd = datetime.date(y + 1, etd.month, etd.day)
                    args_dict = {
                        'group': self,
                        'semester': i,
                        'start_date': std,
                        'end_date': etd,
                    }
                    SemesterSchedule.objects.create(**args_dict)

    def __str__(self):
        return '%s-%s%s' % (
            self.specialty.abbreviation,
            str(self.year % 100),
            self.form.suffix,
        )

    class Meta:
        verbose_name = _('Group stream')
        verbose_name_plural = _('Group streams')
        unique_together = [['specialty', 'year', 'form']]

class SemesterSchedule(models.Model):
    group = models.ForeignKey(
        'GroupStream',
        on_delete=models.CASCADE,
        verbose_name=_('Group stream'),
    )

    semester = models.PositiveSmallIntegerField(
        verbose_name=_('Semester'),
        validators=[MinValueValidator(1)],
    )

    start_date = models.DateField(
        verbose_name=_('Start date'),
        default=None,
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        verbose_name=_('End date'),
        default=None,
        blank=True,
        null=True,
    )

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            error = _("End date should be greater than start date.")
            raise ValidationError(error)
        super(SemesterSchedule, self).clean()

    def __str__(self):
        s = _('{semester} semester')
        string = s.format(semester=self.semester)
        return '%s - %s' % (self.group, string)

    class Meta:
        verbose_name = _('Semester schedule')
        verbose_name_plural = _('Semester schedule')
        unique_together = [['group', 'semester']]

class Group(ReadOnlyOnExistForeignKey, models.Model):
    def generate_number_choices():
        l = [(None,'-')]
        for x in range(1, 9):
            l.append((x, x))
        return l

    NUMBER_CHOICES = generate_number_choices()

    group_stream = models.ForeignKey(
        'GroupStream',
        on_delete=models.CASCADE,
        verbose_name=_('Group stream'),
        default=None,
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name=_('Parent node'),
        default=None,
        blank=True,
        null=True,
    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_('Number'),
        choices=NUMBER_CHOICES,
        default=None,
        blank=True,
        null=True,
    )

    important_fields = ['parent']
    related_models = [
        ('CurriculumEntry', 'group'),
        ('CurriculumEntryTeacher', 'group'),
    ]

    #~ def __init__(self, *args, **kwargs):
        #~ super(Group, self).__init__(*args, **kwargs)
        #~ self.__important_fields = ['parent']
        #~ for field in self.__important_fields:
            #~ setattr(self, '__original_%s' % field, getattr(self, field))

    #~ def has_changed(self):
        #~ for field in self.__important_fields:
            #~ orig = '__original_%s' % field
            #~ if getattr(self, orig) != getattr(self, field):
                #~ return True
        #~ return False

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
        #~ ceb = CurriculumEntry.objects.filter(group=self).exists()
        #~ cetb = CurriculumEntryTeacher.objects.filter(group=self).exists()
        #~ if ceb and cetb and self.has_changed():
            #~ error = _("Parent node can't be changed when {} and {} exists")
            #~ cevn = CurriculumEntry._meta.verbose_name
            #~ cetvn = CurriculumEntryTeacher._meta.verbose_name
            #~ raise ValidationError(error.format(cevn, cetvn))
        if self.parent is not None:
            if self.number is None:
                error = _("Number may not be empty when having parent group class.")
                raise ValidationError(error)
            depth = self.calculate_max_depth_of_childs()
            if depth > MAX_GROUP_TREE_HEIGHT:
                error = _("Group can't have parent group with such depth.")
                raise ValidationError(error)
        super(Group, self).clean()

    def validate_unique(self, exclude=None):
        group_stream = None
        try: group_stream = self.group_stream
        except Group.DoesNotExist as e: pass
        parent = None
        try: parent = self.parent
        except Group.DoesNotExist as e: pass
        if group_stream and parent:
            args = {
                'group_stream': self.group_stream,
                'parent': parent,
                'number': self.number,
            }
            if Group.objects.exclude(id=self.id).filter(**args).exists():
                raise ValidationError(_("Duplicate group node"))
        super(Group, self).validate_unique(exclude)

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
        print("calculate_max_depth_of_childs(%s)" % self)
        return 1 + len(self.get_path_to_root()) + self.calculate_node_height()

    def __str__(self):
        number = [self] + self.get_path_to_root()
        args = (
            str(self.group_stream),
            ''.join('-%s' % i.number for i in reversed(number[:-1])),
        )
        return '%s%s' % args

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        unique_together = [[
            'group_stream', 'parent', 'number'
        ]]

class Curriculum(models.Model):
    group = models.ForeignKey(
        'GroupStream',
        on_delete=models.CASCADE,
        verbose_name=_('Group stream'),
    )
    semester = models.PositiveSmallIntegerField(
        verbose_name=_('Semester'),
    )

    def __str__(self):
        semester = _('{semester} semester').format(semester=self.semester)
        return '%s - %s' % (self.group, semester)

    class Meta:
        verbose_name = _('Curriculum')
        verbose_name_plural = _('Curriculums')
        unique_together = [['group', 'semester']]


class CurriculumEntry(models.Model):
    curriculum = models.ForeignKey(
        'Curriculum',
        on_delete=models.CASCADE,
        verbose_name=_('Curriculum'),
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_('Group'),
    )
    subjects = models.ManyToManyField(
        Subject,
        through='CurriculumEntrySubject',
        verbose_name=_('Subjects'),
    )
    teachers = models.ManyToManyField(
        Teacher,
        through='CurriculumEntryTeacher',
        verbose_name=_('Teachers'),
    )
    lectures = models.PositiveSmallIntegerField(
        verbose_name=_('Number of lectures'),
    )
    practices = models.PositiveSmallIntegerField(
        verbose_name=_('Number of practices'),
    )
    laboratory = models.PositiveSmallIntegerField(
        verbose_name=_('Number of laboratory'),
    )
    independent_work = models.PositiveSmallIntegerField(
        verbose_name=_('Amount of independent work'),
    )

    def clean(self):
        curriculum = None
        group = None
        try: curriculum = self.curriculum
        except Curriculum.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if curriculum and group and group.group_stream != curriculum.group:
            error = _("Group must be child of or same as group in curriculum")
            raise ValidationError(error)
        super(CurriculumEntry, self).clean()

    def get_semester(self):
        return self.curriculum.semester

    def get_subject_name(self):
        return '/'.join(str(i) for i in self.subjects.all())

    def __str__(self):
        subjects = self.get_subject_name()
        if subjects: subjects = ' - ' + subjects
        semester = _('{semester} semester').format(semester=self.get_semester())
        return '%s - %s%s' % (self.group, semester, subjects)

    class Meta:
        verbose_name = _('Curriculum entry')
        verbose_name_plural = _('Curriculum entries')

class CurriculumEntrySubject(models.Model):
    entry = models.ForeignKey(
        'CurriculumEntry',
        on_delete=models.CASCADE,
        verbose_name=_('Curriculum entry'),
    )

    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        verbose_name=_('Subject'),
    )

    def get_group(self):
        return self.entry.group

    def get_semester(self):
        return self.entry.get_semester()

    def __str__(self):
        s = _('{semester} semester')
        string = s.format(semester=self.get_semester())
        return '%s - %s - %s' % (self.get_group(), string, self.subject)

    class Meta:
        verbose_name = _('Subject for curriculum entry')
        verbose_name_plural = _('Subjects for curriculum entries')

class CurriculumEntryTeacher(models.Model):
    RESPONSIBILITY_CHOICES = [
        (0, 'Lectures'),
        (1, 'Practices'),
        (2, 'Laboratory'),
    ]

    entry = models.ForeignKey(
        'CurriculumEntry',
        on_delete=models.CASCADE,
        verbose_name=_('Curriculum entry'),
    )

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_('Group'),
    )

    responsibility = models.PositiveSmallIntegerField(
        verbose_name=_('Responsibility'),
        choices=RESPONSIBILITY_CHOICES,
        default=0,
    )

    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        verbose_name=_('Teacher'),
    )

    def clean(self):
        entry = None
        group = None
        try: entry = self.entry
        except CurriculumEntry.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if entry and group:
            pg = entry.group
            if pg != group and not group.is_child(pg):
                error = _("Group must be child of or same as group in entry")
                raise ValidationError(error)
        super(CurriculumEntryTeacher, self).clean()

    def validate_unique(self, exclude=None):
        entry = None
        group = None
        try: entry = self.entry
        except CurriculumEntry.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if entry and group:
            arr = group.get_path_to_root_and_childs() if group else []
            args = {
                'entry': entry,
                'group__in': arr,
                'responsibility': self.responsibility,
            }
            f = CurriculumEntryTeacher.objects.exclude(id=self.id).filter(**args)
            if f.exists():
                error = _("Duplicate teacher for curriculum entry by group {}.")
                raise ValidationError(error.format(f.first().group))
        super(CurriculumEntryTeacher, self).validate_unique(exclude)

    def __str__(self):
        rc = dict(self.RESPONSIBILITY_CHOICES)
        responsibility = rc[self.responsibility]
        args = (self.group, responsibility, self.teacher)
        return '%s - %s - %s' % args

    class Meta:
        verbose_name = _('Teacher for curriculum entry')
        verbose_name_plural = _('Teachers for curriculum entries')
        unique_together = [[
            'entry', 'group', 'responsibility',
        ]]


class TimetableEntry(models.Model):
    def generate_lesson_choices():
        arr = []
        weeks = (_('numerator'), _('denominator'))
        days = (
            _('mon'), _('tue'), _('wed'), _('thu'), _('fri'),
            _('sat'), _('sun')
        )
        msg = _('{lesson} lesson')
        for ik, iv in enumerate(weeks):
            for j in WORK_DAYS:
                for k in range(1, MAX_LESSONS_DAY + 1):
                    l = msg.format(lesson=k)
                    val = ik * 256 + j * 32 + k
                    arr.append((val, '%s - %s - %s' % (iv, days[j], l)))
        return arr

    LESSON_CHOICES = generate_lesson_choices()

    entry = models.ForeignKey(
        'CurriculumEntry',
        on_delete=models.CASCADE,
        verbose_name=_('Curriculum entry'),
    )

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        verbose_name=_('Group'),
    )

    lesson = models.PositiveSmallIntegerField(
        verbose_name=_('Number of lesson'),
        choices=LESSON_CHOICES,
        default=0,
    )

    classroom = models.ForeignKey(
        'Classroom',
        on_delete=models.CASCADE,
        verbose_name=_('Classroom'),
        default=None,
        null=True,
        blank=True,
    )

    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        verbose_name=_('Teacher'),
        default=None,
        null=True,
        blank=True,
    )

    def clean(self):
        entry = None
        group = None
        try: entry = self.entry
        except CurriculumEntry.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if entry and group:
            pg = entry.group
            if pg != group and not group.is_child(pg):
                error = _("Group must be child of or same as group in curriculum entry")
                raise ValidationError(error)
        super(TimetableEntry, self).clean()

    def validate_unique(self, exclude=None):
        entry = None
        group = None
        try: entry = self.entry
        except CurriculumEntry.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        if group:
            arr = group.get_path_to_root_and_childs()
            args = {
                'entry': entry,
                'group__in': arr,
                'lesson': self.lesson,
            }
            f = TimetableEntry.objects.exclude(id=self.id).filter(**args)
            if f.exists():
                error = _("Duplicate timetable entry by group {}.")
                raise ValidationError(error.format(f.first().group))
        super(TimetableEntry, self).validate_unique(exclude)

    def __str__(self):
        msg = _('{semester} semester')
        semester = msg.format(semester=self.entry.getSemester())
        lesson = dict(self.LESSON_CHOICES)[self.lesson]
        args = (str(self.group), semester, lesson, self.entry.getSubjectName())
        return '%s - %s - %s - %s' % args

    class Meta:
        verbose_name = _('Timetable entry')
        verbose_name_plural = _('Timetable entries')
        unique_together = [
            ['entry', 'group', 'lesson'], ['lesson', 'classroom']
        ]
