from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path

from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField
from django_improvements.admin import (
    AdminBaseWithSelectRelated,
    AdminInlineWithSelectRelated,
    AdminStackedInlineWithSelectRelated,
    AdminWithSelectRelated,
    FilterWithSelectRelated,
)

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

from .forms import (
    FormOfStudySemesterFormset,
    GroupStreamSemesterForm,
)

def generate_list_select_related_for_group(prefix, parent, list_select):
    arr = []
    for i in range(0, MAX_GROUP_TREE_HEIGHT):
        if i > 0:
            t = [prefix] + [parent for i in range(i)]
            arr.append('__'.join(filter(None, t)))
        for j in list_select:
            t = [prefix] + [parent for i in range(i)] + [j]
            arr.append('__'.join(filter(None, t)))
    return arr

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
    search_fields = ('number',)

class FormOfStudySemesterInline(admin.TabularInline):
    model = FormOfStudySemester
    formset = FormOfStudySemesterFormset

@admin.register(FormOfStudy)
class FormOfStudyAdmin(ImportExportModelAdmin):
    inlines = [FormOfStudySemesterInline,]
    list_display = ('name', 'suffix', 'semesters', 'priority',)
    list_filter = ('semesters', 'priority',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name', 'suffix',)

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
    list_filter = ('specialty__faculty', SpecialtyYearFilter, 'form',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('specialty', 'form')
    raw_id_fields = ('specialty',)
    search_fields = (
        'specialty__name', 'specialty__number',
        'specialty__abbreviation', 'year'
    )

class GroupYearFilter(admin.SimpleListFilter):
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
                        'group_stream__year__gte': int(years[0]),
                        'group_stream__year__lte': int(years[1]),
                    }
                    return queryset.filter(**args)
                except ValueError: pass

class GroupInline(AdminInlineWithSelectRelated):
    model = Group
    exclude = ['group_stream',]
    list_select_related = generate_list_select_related_for_group(
        '', 'parent', (
            'group_stream',
            'group_stream__specialty',
            'group_stream__form',
        )
    )

@admin.register(Group)
class GroupAdmin(AdminWithSelectRelated, MPTTModelAdmin, ImportExportModelAdmin):
    inlines = [GroupInline,]
    list_filter = (
        'group_stream__specialty__faculty', GroupYearFilter,
        'group_stream__form',
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = generate_list_select_related_for_group(
        '', 'parent', (
            'group_stream',
            'group_stream__specialty',
            'group_stream__form',
        )
    )
    raw_id_fields = ('group_stream', 'parent',)
    search_fields = (
        'group_stream__specialty__name',
        'group_stream__specialty__number',
        'group_stream__specialty__abbreviation',
        'group_stream__year',
        'number',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj: return ['group_stream', 'parent',]
        else: return []

class CurriculumRecordInline(admin.StackedInline):
    model = CurriculumRecord
    raw_id_fields = ('group',)

@admin.register(Curriculum)
class CurriculumAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    inlines = [
        CurriculumRecordInline,
    ]
    list_filter = (
        'group__specialty__faculty', SpecialtyYearFilter,
        'group__form', 'semester',
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = [
        'group',
        'group__specialty',
        'group__form',
    ]
    raw_id_fields = ('group',)
    search_fields = (
        'group__specialty__name', 'group__specialty__number',
        'group__specialty__abbreviation', 'group__year'
    )

class CurriculumRecordSubjectInline(admin.TabularInline):
    model = CurriculumRecord.subjects.through

class CurriculumRecordTeacherInline(AdminInlineWithSelectRelated):
    model = CurriculumRecord.teachers.through
    #~ form = CurriculumRecordTeacherInlineForm
    #~ raw_id_fields = ('teacher',)
    list_select_related = generate_list_select_related_for_group(
        'group', 'parent', (
            'group_stream',
            'group_stream__specialty',
            'group_stream__form',
        )
    ) + [
        'teacher', 'teacher__person',
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        obj = request._obj_
        if db_field.name == "group":
            if obj is not None:
                filter_dict = {
                    'group_stream__exact': obj.group.group_stream_id,
                }
                query = Group.objects.filter(**filter_dict)
                return TreeNodeChoiceField(query)
            else:
                return TreeNodeChoiceField(Group.objects.none())
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "teacher":
            if obj is not None:
                departments = [i.department_id for i in obj.subjects.all()]
                filter_dict = {
                    'department__in': departments,
                }
                field.queryset = field.queryset.filter(**filter_dict)
            else:
                field.queryset = field.queryset.none()
        return field

@admin.register(CurriculumRecord)
class CurriculumRecordAdmin(ImportExportModelAdmin):
    inlines = [
        CurriculumRecordSubjectInline,
        CurriculumRecordTeacherInline,
    ]
    raw_id_fields = ('curriculum', 'group',)

    def get_inline_instances(self, request, obj=None):
        if obj: return [inline(self.model, self.admin_site) for inline in self.inlines]
        else: return []

    def get_readonly_fields(self, request, obj=None):
        if obj: return ['curriculum', 'group',]
        else: return []

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(CurriculumRecordAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(TimetableRecording)
