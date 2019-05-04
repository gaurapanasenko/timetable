from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path

from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin

from .settings import *

from .models import Faculty
from .models import Department
from .models import Subject
from .models import Person
from .models import Teacher
from .models import Specialty
from .models import FormOfStudy
from .models import FormOfStudySemester
from .models import GroupStream
from .models import Group
from .models import Building
from .models import Classroom
from .models import Curriculum
from .models import CurriculumRecord
from .models import GroupStreamSemester
from .models import TimetableRecording

from .forms import FormOfStudySemesterFormset

class CurriculumRecordInline(admin.TabularInline):
    model = CurriculumRecord

class CurriculumAdmin(admin.ModelAdmin):
    inlines = [
        CurriculumRecordInline,
    ]

class CurriculumRecordSubjectInline(admin.TabularInline):
    model = CurriculumRecord.subjects.through

class CurriculumRecordTeacherInline(admin.TabularInline):
    model = CurriculumRecord.teachers.through

class CurriculumRecordAdmin(admin.ModelAdmin):
    inlines = [
        CurriculumRecordSubjectInline,
        CurriculumRecordTeacherInline,
    ]

@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'abbreviation',)
    search_fields = ('name', 'abbreviation',)

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name', 'faculty', 'abbreviation',)
    search_fields = (
        'name', 'faculty__name',
        'faculty__abbreviation', 'abbreviation',
    )
    list_filter = ('faculty', )

class DepartmentFacultyFilter(admin.SimpleListFilter):
    title = _('faculty')
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
    search_fields = (
        'name', 'department__name', 'department__faculty__name',
        'department__faculty__abbreviation', 'department__abbreviation',
    )
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
    search_fields = (
        'person__first_name', 'person__middle_name', 'person__last_name',
        'department__name', 'department__faculty__name',
        'department__faculty__abbreviation', 'department__abbreviation',
    )
    list_filter = (DepartmentFacultyFilter,)
    raw_id_fields = ('department',)

@admin.register(Specialty)
class SpecialtyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'number', 'abbreviation', 'faculty',)
    search_fields = (
        'name', 'number', 'abbreviation',
        'faculty__name', 'faculty__abbreviation',
    )
    list_filter = ('faculty',)

@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    list_display = ('number', 'address',)
    search_fields = ('number', 'address',)

@admin.register(Classroom)
class ClassroomAdmin(ImportExportModelAdmin):
    list_display = ('building', 'number',)
    search_fields = ('building__number', 'building__address', 'number',)
    list_filter = ('building',)

class FormOfStudySemesterInline(admin.TabularInline):
    model = FormOfStudySemester
    formset = FormOfStudySemesterFormset

@admin.register(FormOfStudy)
class FormOfStudyAdmin(ImportExportModelAdmin):
    list_display = ('name', 'suffix', 'semesters', 'priority',)
    search_fields = ('name', 'suffix', 'semesters', 'priority',)
    list_filter = ('semesters', 'priority',)
    inlines = [FormOfStudySemesterInline,]

class SpecialtyYearFilter(admin.SimpleListFilter):
    title = _('year')
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
    title = _('faculty')
    parameter_name = 'faculty'

    def lookups(self, request, model_admin):
        return ((i.id, str(i)) for i in Faculty.objects.all())

    def queryset(self, request, queryset):
        if self.value():
            try:
                arr = Specialty.objects.filter(faculty=self.value()).all()
                return queryset.filter(specialty__in=arr)
            except ValueError: pass

class GroupStreamSemesterInline(admin.TabularInline):
    model = GroupStreamSemester

@admin.register(GroupStream)
class GroupStreamAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'specialty', 'year', 'form',)
    search_fields = (
        'specialty__name', 'specialty__number',
        'specialty__abbreviation',
        'specialty__faculty__name', 'specialty__faculty__abbreviation',
        'year', 'form__name', 'form__suffix',
        'form__semesters', 'form__priority',
    )
    list_filter = (SpecialtyFacultyFilter, 'form', SpecialtyYearFilter,)
    raw_id_fields = ('specialty',)
    inlines = [
        GroupStreamSemesterInline,
    ]

class GroupInline(admin.TabularInline):
    model = Group

@admin.register(Group)
class GroupAdmin(MPTTModelAdmin):
    #~ search_fields = ('specialty', 'year', 'form',)
    #~ list_filter = (SpecialtyFacultyFilter, 'form', SpecialtyYearFilter,)
    #~ raw_id_fields = ('specialty',)
    inlines = [GroupInline,]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['group_stream', 'parent', 'number',]
        else:
            return []

admin.site.register(Curriculum, CurriculumAdmin)

admin.site.register(CurriculumRecord, CurriculumRecordAdmin)

admin.site.register(TimetableRecording)
