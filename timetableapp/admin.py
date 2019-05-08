from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path

from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin
from django_improvements.admin import AdminBaseWithSelectRelated
from django_improvements.admin import AdminInlineWithSelectRelated
from django_improvements.admin import AdminWithSelectRelated
from django_improvements.admin import FilterWithSelectRelated

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

from .forms import FormOfStudySemesterFormset, GroupStreamSemesterForm

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
    list_per_page = LIST_PER_PAGE
    search_fields = ('name', 'abbreviation',)


@admin.register(Department)
class DepartmentAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('name', 'faculty', 'abbreviation',)
    list_filter = ('faculty', )
    list_per_page = LIST_PER_PAGE
    list_select_related = ('faculty',)
    search_fields = (
        'name',
        'faculty__name', 'faculty__abbreviation',
        'abbreviation',
    )

@admin.register(Subject)
class SubjectAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('name', 'department',)
    list_filter = ('department__faculty',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('department',)
    raw_id_fields = ('department',)
    search_fields = (
        'name', 'department__name', 'department__faculty__name',
        'department__faculty__abbreviation', 'department__abbreviation',
    )

@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('first_name', 'middle_name', 'last_name',)

@admin.register(Teacher)
class TeacherAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('person', 'department',)
    list_filter = ('department__faculty',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('person', 'department', )
    raw_id_fields = ('department',)
    search_fields = (
        'person__first_name', 'person__middle_name',
        'person__last_name',
        'department__name',
        'department__faculty__name',
        'department__faculty__abbreviation',
        'department__abbreviation',
    )

@admin.register(Specialty)
class SpecialtyAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('name', 'number', 'abbreviation', 'faculty',)
    list_filter = ('faculty',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('faculty',)
    search_fields = (
        'name', 'number', 'abbreviation',
        'faculty__name', 'faculty__abbreviation',
    )

@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    list_display = ('number', 'address',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('number', 'address',)

@admin.register(Classroom)
class ClassroomAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('building', 'number',)
    list_filter = ('building',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('building',)
    search_fields = ('building__number', 'building__address', 'number',)

class FormOfStudySemesterInline(admin.TabularInline):
    model = FormOfStudySemester
    formset = FormOfStudySemesterFormset

@admin.register(FormOfStudy)
class FormOfStudyAdmin(ImportExportModelAdmin):
    inlines = [FormOfStudySemesterInline,]
    list_display = ('name', 'suffix', 'semesters', 'priority',)
    list_filter = ('semesters', 'priority',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name', 'suffix', 'semesters', 'priority',)

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

class GroupStreamSemesterInline(admin.TabularInline):
    model = GroupStreamSemester
    form = GroupStreamSemesterForm

@admin.register(GroupStream)
class GroupStreamAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    inlines = [
        GroupStreamSemesterInline,
    ]
    list_display = ('__str__', 'specialty', 'year', 'form',)
    list_filter = ('specialty__faculty', SpecialtyYearFilter,)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('specialty', 'form')
    raw_id_fields = ('specialty',)
    search_fields = (
        'specialty__name', 'specialty__number',
        'specialty__abbreviation',
        'specialty__faculty__name', 'specialty__faculty__abbreviation',
        'year', 'form__name', 'form__suffix',
        'form__semesters', 'form__priority',
    )

class GroupInline(AdminInlineWithSelectRelated):
    model = Group
    exclude = ['group_stream',]
    list_select_related = (
        'parent',
        'parent__group_stream',
        'parent__group_stream__specialty',
        'parent__group_stream__form',
        'group_stream',
        'group_stream__specialty',
        'group_stream__form',
    )

@admin.register(Group)
class GroupAdmin(AdminWithSelectRelated, MPTTModelAdmin, ImportExportModelAdmin):
    #~ search_fields = ('specialty', 'year', 'form',)
    #~ list_filter = (SpecialtyFacultyFilter, 'form', SpecialtyYearFilter,)
    #~ raw_id_fields = ('specialty',)
    inlines = [GroupInline,]
    list_per_page = LIST_PER_PAGE
    list_select_related = (
        'parent',
        'parent__group_stream',
        'parent__group_stream__specialty',
        'parent__group_stream__form',
        'group_stream',
        'group_stream__specialty',
        'group_stream__form',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return []
            #~ return ['group_stream', 'parent', 'number',]
        else:
            return []

admin.site.register(Curriculum, CurriculumAdmin)

admin.site.register(CurriculumRecord, CurriculumRecordAdmin)

admin.site.register(TimetableRecording)
