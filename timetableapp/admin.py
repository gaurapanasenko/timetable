from django.contrib import admin

from .models import Faculty
from .models import Department
from .models import Subject
from .models import Person
from .models import Teacher
from .models import Specialty
from .models import GroupState
from .models import GroupStream
from .models import Group
from .models import Building
from .models import Classroom
from .models import Curriculum
from .models import CurriculumEntry
from .models import SemesterSchedule
from .models import TimetableEntry

class CurriculumEntryInline(admin.TabularInline):
    model = CurriculumEntry

class CurriculumAdmin(admin.ModelAdmin):
    inlines = [
        CurriculumEntryInline,
    ]

class CurriculumEntrySubjectInline(admin.TabularInline):
    model = CurriculumEntry.subjects.through

class CurriculumEntryTeacherInline(admin.TabularInline):
    model = CurriculumEntry.teachers.through

class CurriculumEntryAdmin(admin.ModelAdmin):
    inlines = [
        CurriculumEntrySubjectInline,
        CurriculumEntryTeacherInline,
    ]

class SemesterScheduleInline(admin.TabularInline):
    model = SemesterSchedule

class GroupInline(admin.TabularInline):
    model = Group

class GroupStreamAdmin(admin.ModelAdmin):
    inlines = [
        SemesterScheduleInline,
        GroupInline,
    ]

admin.site.register(Faculty)

admin.site.register(Department)

admin.site.register(Subject)

admin.site.register(Person)

admin.site.register(Teacher)

admin.site.register(Specialty)

admin.site.register(Building)

admin.site.register(Classroom)

admin.site.register(GroupState)

admin.site.register(GroupStream, GroupStreamAdmin)

admin.site.register(Group)

admin.site.register(Curriculum, CurriculumAdmin)

admin.site.register(CurriculumEntry, CurriculumEntryAdmin)

admin.site.register(TimetableEntry)
