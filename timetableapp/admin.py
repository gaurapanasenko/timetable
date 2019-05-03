from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render
from django.shortcuts import redirect

from import_export.admin import ImportExportModelAdmin

#~ from .forms import SubjectForm

from .settings import *

from .models import Faculty
from .models import Department
from .models import Subject
from .models import Person
from .models import Teacher
from .models import Specialty
from .models import FormOfStudy
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

@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'abbreviation',)
    search_fields = ('name', 'abbreviation',)

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'faculty', 'abbreviation',)
    search_fields = ('name', 'faculty', 'abbreviation',)
    list_filter = ('faculty', )

class DepartmentFacultyFilter(admin.SimpleListFilter):
    title = _('Faculty')
    parameter_name = 'faculty'

    def lookups(self, request, model_admin):
        return ((i.id, str(i)) for i in Faculty.objects.all())

    def queryset(self, request, queryset):
        if self.value():
            arr = Department.objects.filter(faculty=self.value()).all()
            return queryset.filter(department__in=arr)

@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('name', 'department',)
    search_fields = ('name', 'department',)
    list_filter = (DepartmentFacultyFilter,)
    raw_id_fields = ('department',)
    #~ form = SubjectForm

@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name',)
    search_fields = ('first_name', 'middle_name', 'last_name',)

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    list_display = ('person', 'department',)
    search_fields = ('person', 'department',)
    list_filter = (DepartmentFacultyFilter,)
    raw_id_fields = ('department',)

@admin.register(Specialty)
class SpecialtyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'number', 'abbreviation', 'faculty',)
    search_fields = ('name', 'number', 'abbreviation', 'faculty',)
    list_filter = ('faculty',)

@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    list_display = ('number', 'address',)
    search_fields = ('number', 'address',)

@admin.register(Classroom)
class ClassroomAdmin(ImportExportModelAdmin):
    list_display = ('building', 'number',)
    search_fields = ('building', 'number',)
    list_filter = ('building', )

@admin.register(FormOfStudy)
class FormOfStudyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'suffix', 'semesters', 'priority',)
    search_fields = ('name', 'suffix', 'semesters', 'priority',)
    list_filter = ('semesters', 'priority',)

class SpecialtyYearFilter(admin.SimpleListFilter):
    title = _('Year')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        arr = []
        for i in range(0, 5):
            year = current_year() - i
            arr.append(('{0}-{0}'.format(year), year))
        for i in reversed(range(START_YEAR, year + 5, 10)):
            year = '{0}-{1}'.format(i, i + 10)
            arr.append((year, year))
        return arr

    def queryset(self, request, queryset):
        if self.value():
            years = self.value().split('-')
            if len(years) == 2:
                try:
                    args = {
                        'year__gte': int(years[0]),
                        'year__lte': int(years[1]),
                    }
                    return queryset.filter(**args)
                except ValueError: pass

class SpecialtyFacultyFilter(admin.SimpleListFilter):
    title = _('Faculty')
    parameter_name = 'faculty'

    def lookups(self, request, model_admin):
        return ((i.id, str(i)) for i in Faculty.objects.all())

    def queryset(self, request, queryset):
        if self.value():
            try:
                arr = Specialty.objects.filter(faculty=self.value()).all()
                return queryset.filter(specialty__in=arr)
            except ValueError: pass

class SemesterScheduleInline(admin.TabularInline):
    model = SemesterSchedule

class GroupInline(admin.TabularInline):
    model = Group

@admin.register(GroupStream)
class GroupStreamAdmin(admin.ModelAdmin):
    list_display = ('specialty', 'year', 'form',)
    search_fields = ('specialty', 'year', 'form',)
    list_filter = (SpecialtyFacultyFilter, 'form', SpecialtyYearFilter,)
    raw_id_fields = ('specialty',)
    inlines = [
        SemesterScheduleInline,
        GroupInline,
    ]

admin.site.register(Group)

admin.site.register(Curriculum, CurriculumAdmin)

admin.site.register(CurriculumEntry, CurriculumEntryAdmin)

admin.site.register(TimetableEntry)
