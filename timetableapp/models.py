from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime

start_year = 1900
current_year = datetime.datetime.now().year
future_diff = 5

class Faculty(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=128,
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_("Abbreviation"),
        max_length=128,
        unique=True,
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Faculty")
        verbose_name_plural = _("Faculties")

class Department(models.Model):
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.PROTECT,
        verbose_name=_("Faculty"),
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=128,
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_("Abbreviation"),
        max_length=128,
        unique=True,
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        return self.abbreviation if self.abbreviation else self.name

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

class Subject(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=128,
        unique=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name=_("Department"),
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

class Person(models.Model):
    firstName = models.CharField(
        verbose_name=_("First name"),
        max_length=128,
    )

    middleName = models.CharField(
        verbose_name=_("Middle name"),
        max_length=128,
    )

    lastName = models.CharField(
        verbose_name=_("Last name"),
        max_length=128,
    )

    def __str__(self):
        args = (self.firstName, self.middleName, self.lastName)
        return "%s %s %s" % args

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        unique_together = [['firstName', 'middleName', 'lastName']]

class Teacher(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name=_("Person"),
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name=_("Department"),
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "%s" % self.person

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

class Specialty(models.Model):
    number = models.PositiveSmallIntegerField(
        verbose_name=_("Number"),
        unique=True,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=128,
        unique=True,
    )
    abbreviation = models.CharField(
        verbose_name=_("Abbreviation"),
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Specialty")
        verbose_name_plural = _("Specialties")

class GroupState(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=128,
        unique=True,
    )
    suffix = models.CharField(
        verbose_name=_("Suffix"),
        max_length=16,
        blank=True,
        unique=True,
    )
    semesters = models.PositiveSmallIntegerField(
        verbose_name=_("Number of semesters"),
        default=8,
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name=_("Priority"),
        choices=((x, x) for x in range(1,10)),
        default=5,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Group state")
        verbose_name_plural = _("Group states")

class Group(models.Model):
    def generateYearsChoices():
        r = reversed(range(start_year, current_year + 1))
        return ((x, x) for x in r)

    def generateNumberChoices():
        l = [(None,"-")]
        for x in range(1, 9):
            l.append((x, x))
        return l

    YEARS_CHOICES = generateYearsChoices()

    NUMBER_CHOICES = generateNumberChoices()

    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        verbose_name=_("Specialty"),
    )
    year = models.PositiveSmallIntegerField(
        verbose_name=_("Year"),
        choices=YEARS_CHOICES,
        default=current_year,
    )
    state = models.ForeignKey(
        GroupState,
        on_delete=models.PROTECT,
        verbose_name=_("State"),
        default={"priority": 1},
    )
    parentId = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name=_("Parent group class"),
        default=None,
        blank=True,
        null=True,

    )
    number = models.PositiveSmallIntegerField(
        verbose_name=_("Number"),
        choices=NUMBER_CHOICES,
        default=None,
        blank=True,
        null=True,
    )

    def clean(self):
        if self.parentId is not None:
            p = self.parentId
            self.specialty = p.specialty
            self.year = p.year
            self.state = p.state
            if self.number is None:
                error = _(
                    'Number entries may not be empty ' +
                    'when have parent group class.'
                )
                raise ValidationError(error)
            k = 1
            while p is not None:
                if k > 2:
                    error = _(
                        'I can\'t create such group tree depth'
                    )
                    raise ValidationError(error)
                k += 1
                p = p.parentId
        elif self.number is not None:
                self.number = None
        super(Group, self).clean()

    def validate_unique(self, exclude=None):
        specialty = None
        try: specialty = self.specialty
        except Specialty.DoesNotExist as e: pass
        args = {
            "specialty": specialty,
            "year": self.year,
            "state": self.state,
            "parentId": self.parentId,
            "number": self.number,
        }
        if Group.objects.exclude(id=self.id).filter(**args).exists():
            raise ValidationError(_("Duplicate group"))
        super(Group, self).validate_unique(exclude)

    def __str__(self):
        number = []
        if self.number:
            number.append(self.number)
        parent = self.parentId
        while parent is not None:
            if parent.number is not None:
                number.append(parent.number)
            parent = parent.parentId
        args = (
            self.specialty.abbreviation,
            str(self.year % 100),
            self.state.suffix,
            "".join("-%s" % i for i in reversed(number)),
        )
        return "%s-%s%s%s" % args

    def getRootPath(self):
        arr = []
        p = self.parentId
        while p is not None:
            arr.append(p)
            p = p.parentId
        return arr

    def getChilds(self):
        arr = []
        childs = Group.objects.filter(parentId=self)
        arr += childs
        for i in childs:
            arr += i.getChilds()
        return arr

    def getRootPathAndChilds(self):
        return [self] + self.getRootPath() + self.getChilds()

    def isChild(self, parent):
        p = self.parentId
        while p is not None:
            if p == parent:
                return True
            p = p.parentId
        return False

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        unique_together = [[
            'specialty', 'year', 'state', 'parentId', 'number'
        ]]

class CurriculumEntry(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name=_("Group"),
    )
    semester = models.PositiveSmallIntegerField(
        verbose_name=_("Semester"),
    )
    subjects = models.ManyToManyField(
        Subject,
        through='CurriculumEntrySubject',
        verbose_name=_("Subjects"),
    )
    teachers = models.ManyToManyField(
        Teacher,
        through='CurriculumEntryTeacher',
        verbose_name=_("Teachers"),
    )
    lectures = models.PositiveSmallIntegerField(
        verbose_name=_("Number of lectures"),
    )
    practices = models.PositiveSmallIntegerField(
        verbose_name=_("Number of practices"),
    )
    laboratory = models.PositiveSmallIntegerField(
        verbose_name=_("Number of laboratory"),
    )
    independentWork = models.PositiveSmallIntegerField(
        verbose_name=_("Amount of independent work"),
    )

    def clean(self):
        max_semester = self.group.state.semesters
        if self.semester > max_semester:
            error = _(
                'Can\'t create semester more than {} for this group'
            ).format(max_semester)
            raise ValidationError(error)
        super(CurriculumEntry, self).clean()

    def validate_unique(self, exclude=None):
        #~ subject = None
        #~ group = None
        #~ try: subjects = self.subjects
        #~ except Subject.DoesNotExist as e: pass
        #~ try: group = self.group
        #~ except Group.DoesNotExist as e: pass
        #~ arr = []
        #~ if group is not None:
            #~ arr = [group] + group.getRootPath() + group.getChilds()
        #~ args = {
            #~ "group__in": arr,
            #~ "semester": self.semester,
        #~ }
        #~ f = CurriculumEntry.objects.exclude(id=self.id).filter(**args)
        #~ if f.exists():
            #~ msg = _("Duplicate curriculum for subject by group {}.")
            #~ raise ValidationError(msg.format(f.first().group))
        super(CurriculumEntry, self).validate_unique(exclude)

    def __str__(self):
        subjects = "/".join(str(i) for i in self.subjects.all())
        if subjects:
            subjects = " - " + subjects
        args = (self.group, self.semester, subjects)
        return "%s - %s%s" % args

    class Meta:
        verbose_name = _("Curriculum entry")
        verbose_name_plural = _("Curriculum entries")

class CurriculumEntrySubject(models.Model):
    entry = models.ForeignKey(
        CurriculumEntry,
        on_delete=models.CASCADE,
        verbose_name=_("Curriculum entry"),
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name=_("Subject"),
    )

    def __str__(self):
        return "%s" % self.subject

    class Meta:
        verbose_name = _("Subject for curriculum entry")
        verbose_name_plural = _("Subjects for curriculum entries")

class CurriculumEntryTeacher(models.Model):
    RESPONSIBILITY_CHOICES = [
        (0, "Lectures"),
        (1, "Practices"),
        (2, "Laboratory"),
    ]

    entry = models.ForeignKey(
        CurriculumEntry,
        on_delete=models.CASCADE,
        verbose_name=_("Curriculum entry"),
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name=_("Subject"),
    )

    responsibility = models.PositiveSmallIntegerField(
        verbose_name=_("Responsibility"),
        choices=RESPONSIBILITY_CHOICES,
        default=0,
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name=_("Lecturer"),
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
            if pg != group and not group.isChild(pg):
                msg = _("Group must be child of or same as group in entry")
                raise ValidationError(msg)
        super(CurriculumEntryTeacher, self).clean()

    def validate_unique(self, exclude=None):
        entry = None
        group = None
        try: entry = self.entry
        except CurriculumEntry.DoesNotExist as e: pass
        try: group = self.group
        except Group.DoesNotExist as e: pass
        arr = group.getRootPathAndChilds() if group else []
        args = {
            'entry': entry,
            'group__in': arr,
            'responsibility': self.responsibility,
        }
        f = CurriculumEntryTeacher.objects.exclude(id=self.id).filter(**args)
        if f.exists():
            msg = _("Duplicate teacher for curriculum entry by group {}.")
            raise ValidationError(msg.format(f.first().group))
        super(CurriculumEntryTeacher, self).validate_unique(exclude)

    def __str__(self):
        rc = dict(self.RESPONSIBILITY_CHOICES)
        responsibility = rc[self.responsibility]
        args = (self.group, responsibility, self.teacher)
        return "%s - %s - %s" % args

    class Meta:
        verbose_name = _("Teacher for curriculum entry")
        verbose_name_plural = _("Teachers for curriculum entries")
        unique_together = [[
            'entry', 'group', 'responsibility',
        ]]
