from django.contrib import admin

from .models import Faculty
from .models import Department
from .models import Subject
from .models import Person
from .models import Teacher
from .models import Specialty
from .models import GroupState
from .models import Group
from .models import CurriculumEntry

class CurriculumEntrySubjectInline(admin.TabularInline):
    model = CurriculumEntry.subjects.through

class CurriculumEntryTeacherInline(admin.TabularInline):
    model = CurriculumEntry.teachers.through

class CurriculumEntryAdmin(admin.ModelAdmin):
    inlines = [
        CurriculumEntrySubjectInline,
        CurriculumEntryTeacherInline,
    ]
    exclude = ('subjects',)

admin.site.register(Faculty)

admin.site.register(Department)

admin.site.register(Subject)

admin.site.register(Person)

admin.site.register(Teacher)

admin.site.register(Specialty)

admin.site.register(GroupState)

admin.site.register(Group)

admin.site.register(CurriculumEntry, CurriculumEntryAdmin)
