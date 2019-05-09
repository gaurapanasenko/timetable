import json

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
    #~ CurriculumRecordAdminForm,
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
    search_fields = ('name', 'abbreviation',)

@admin.register(Subject)
class SubjectAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('name', 'department',)
    list_filter = ('department__faculty',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('department',)
    autocomplete_fields = ('department',)
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
    autocomplete_fields = ('department',)
    search_fields = (
        'person__first_name', 'person__middle_name',
        'person__last_name',
        'department__name',
        'department__abbreviation',
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        p = request.path.find('/autocomplete') != -1
        f = 'filter' in request.GET
        if request.is_ajax() and p and f:
            filter_dict = json.loads(request.GET['filter'])
            queryset = queryset.filter(**filter_dict)
        return queryset, use_distinct

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

class YearFilter(admin.SimpleListFilter):
    title = _('year')
    parameter_name = 'year'
    year_field_path = ''

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
                    fp = self.year_field_path
                    args = {
                        '%syear__gte' % fp: int(years[0]),
                        '%syear__lte' % fp: int(years[1]),
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
    list_filter = ('specialty__faculty', YearFilter, 'form',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('specialty', 'form')
    autocomplete_fields = ('specialty',)
    search_fields = (
        'specialty__name', 'specialty__number',
        'specialty__abbreviation', 'year'
    )

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

class GroupStreamYearFilter(YearFilter):
    year_field_path = 'group_stream__'

@admin.register(Group)
class GroupAdmin(AdminWithSelectRelated, MPTTModelAdmin, ImportExportModelAdmin):
    inlines = [GroupInline,]
    list_filter = (
        'group_stream__specialty__faculty', GroupStreamYearFilter,
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
    autocomplete_fields = ('group_stream', 'parent',)
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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        p = request.path.find('/autocomplete') != -1
        f = 'filter' in request.GET
        if request.is_ajax() and p and f:
            filter_dict = json.loads(request.GET['filter'])
            queryset = queryset.filter(**filter_dict)
        return queryset, use_distinct

class CurriculumRecordInline(AdminStackedInlineWithSelectRelated):
    model = CurriculumRecord
    #~ form = CurriculumRecordAdminForm
    autocomplete_fields = ('group', 'subjects',)
    list_select_related =  generate_list_select_related_for_group(
        'group', 'parent', (
            'group_stream',
            'group_stream__specialty',
            'group_stream__form',
        )
    ) + [
        'curriculum',
        'curriculum__group__specialty',
        'curriculum__group__form',
    ]

class GroupYearFilter(YearFilter):
    year_field_path = 'group__'

@admin.register(Curriculum)
class CurriculumAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    inlines = [
        CurriculumRecordInline,
    ]
    list_display = ('group', 'semester',)
    list_filter = (
        'group__specialty__faculty', GroupYearFilter,
        'group__form', 'semester',
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = [
        'group',
        'group__specialty',
        'group__form',
    ]
    autocomplete_fields = ('group',)
    search_fields = (
        'group__specialty__name', 'group__specialty__number',
        'group__specialty__abbreviation', 'group__year'
    )

class GroupGroupStreamYearFilter(YearFilter):
    year_field_path = 'group__group_stream__'

class CurriculumRecordTeacherInline(admin.StackedInline):
    model = CurriculumRecord.teachers.through
    autocomplete_fields = ('group', 'teacher',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        obj = request._obj_
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "group":
            if obj is not None:
                filter_dict = {
                    'group_stream__exact': obj.group.group_stream_id,
                }
                field.widget.attrs['data-filter'] = json.dumps(filter_dict)
                field.queryset = field.queryset.filter(**filter_dict)
            else:
                filter_dict = {'group_stream__exact': 0}
                field.widget.attrs['data-filter'] = json.dumps(filter_dict)
                field.queryset = field.queryset.none()
        if db_field.name == "teacher":
            if obj is not None:
                departments = [i.department_id for i in obj.subjects.all()]
                filter_dict = {'department__in': departments}
                field.widget.attrs['data-filter'] = json.dumps(filter_dict)
                field.queryset = field.queryset.filter(**filter_dict)
            else:
                filter_dict = {'department__in': 0}
                field.widget.attrs['data-filter'] = json.dumps(filter_dict)
                field.queryset = field.queryset.none()
        return field

@admin.register(CurriculumRecord)
class CurriculumRecordAdmin(ImportExportModelAdmin):
    #~ list_display = ('__str__', 'specialty', 'year', 'form',)
    list_filter = (
        'curriculum__group__specialty__faculty',
        GroupGroupStreamYearFilter,
        'curriculum__group__form', 'curriculum__semester',
    )
    list_per_page = LIST_PER_PAGE
    #~ list_select_related = [
        #~ 'cir',
        #~ 'group__specialty',
        #~ 'group__form',
    #~ ]
    autocomplete_fields = ('curriculum', 'group', 'subjects', )
    #~ search_fields = (
        #~ 'group__specialty__name', 'group__specialty__number',
        #~ 'group__specialty__abbreviation', 'group__year'
    #~ )

    def get_inline_instances(self, request, obj=None):
        if obj:
            return [CurriculumRecordTeacherInline(self.model, self.admin_site)]
        else: return []

    def get_readonly_fields(self, request, obj=None):
        if obj: return ['curriculum', 'group',]
        else: return []

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(CurriculumRecordAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(TimetableRecording)
