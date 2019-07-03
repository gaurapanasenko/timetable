import json, regex

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, reverse
from django.db.models import Q
from django.template.defaultfilters import escape
from django.utils.safestring import mark_safe

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
from admin_auto_filters.filters import AutocompleteFilter

from .settings import *

from .models import (
    Faculty,
    Department,
    Subject,
    Person,
    Teacher,
    Specialty,
    FormOfStudy,
    FormOfStudySemester,
    GroupStream,
    Group,
    Building,
    Classroom,
    Curriculum,
    CurriculumRecord,
    TimetableRecording
)

from .forms import (
    FormOfStudySemesterFormset,
    CurriculumForm,
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

class DepartmentInline(admin.TabularInline):
    model = Department
    show_change_link = True

class SpecialtyInline(admin.TabularInline):
    model = Specialty
    show_change_link = True

@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    inlines = [DepartmentInline, SpecialtyInline,]
    list_display = ('name', 'abbreviation',)
    list_display_links = ('name', 'abbreviation',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name', 'abbreviation',)

class SubjectInline(admin.TabularInline):
    model = Subject
    show_change_link = True

class TeacherInline(admin.TabularInline):
    model = Teacher
    autocomplete_fields = ('person',)
    show_change_link = True

@admin.register(Department)
class DepartmentAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    inlines = [SubjectInline, TeacherInline,]
    list_display = ('name', 'faculty_link', 'abbreviation',)
    list_filter = ('faculty', )
    list_per_page = LIST_PER_PAGE
    list_select_related = ('faculty',)
    search_fields = ('name', 'abbreviation',)

    def faculty_link(self, obj=None):
        if obj and obj.faculty_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_faculty_change", args=(obj.faculty_id,)) , escape(obj.faculty)))
        else: return '-'
    faculty_link.short_description = _("faculty")
    faculty_link.admin_order_field = 'faculty'

@admin.register(Subject)
class SubjectAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('name', 'department_link',)
    list_filter = ('department__faculty',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('department',)
    autocomplete_fields = ('department',)
    search_fields = (
        'name', 'department__name', 'department__faculty__name',
        'department__faculty__abbreviation', 'department__abbreviation',
    )

    def department_link(self, obj=None):
        if obj and obj.department_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_department_change", args=(obj.department_id,)) , escape(obj.department)))
        else: return '-'
    department_link.short_description = _("department")
    department_link.admin_order_field = 'department'

@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    inlines = [TeacherInline,]
    list_display = ('first_name', 'middle_name', 'last_name',)
    list_display_links = ('first_name', 'middle_name', 'last_name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('first_name', 'middle_name', 'last_name',)

@admin.register(Teacher)
class TeacherAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('__str__', 'person_link', 'department_link',)
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

    def person_link(self, obj=None):
        if obj and obj.person_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_person_change", args=(obj.person_id,)) , escape(obj.person)))
        else: return '-'
    person_link.short_description = _("person")
    person_link.admin_order_field = 'person'

    def department_link(self, obj=None):
        if obj and obj.department_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_department_change", args=(obj.department_id,)) , escape(obj.department)))
        else: return '-'
    department_link.short_description = _("department")
    department_link.admin_order_field = 'department'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        p = request.path.find('/autocomplete') != -1
        f = 'filter' in request.GET
        if request.is_ajax() and p and f:
            filter_dict = json.loads(request.GET['filter'])
            queryset = queryset.filter(**filter_dict)
        return queryset, use_distinct

class GroupStreamInline(admin.TabularInline):
    model = GroupStream
    show_change_link = True

    def get_queryset(self, request):
        qs = super(GroupStreamInline, self).get_queryset(request)
        return qs.filter(year=current_year())

@admin.register(Specialty)
class SpecialtyAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    inlines = [GroupStreamInline,]
    list_display = ('name', 'number', 'abbreviation', 'faculty_link',)
    list_filter = ('faculty',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('faculty',)
    search_fields = (
        'name', 'number', 'abbreviation',
        'faculty__name', 'faculty__abbreviation',
    )

    def faculty_link(self, obj=None):
        if obj and obj.faculty_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_faculty_change", args=(obj.faculty_id,)) , escape(obj.faculty)))
        else: return '-'
    faculty_link.short_description = _("faculty")
    faculty_link.admin_order_field = 'faculty'

class ClassroomInline(admin.TabularInline):
    model = Classroom
    show_change_link = True

@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    inlines = [ClassroomInline,]
    list_display = ('number', 'address',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('number', 'address',)

@admin.register(Classroom)
class ClassroomAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('__str__', 'building_link', 'number',)
    list_display_links = ('__str__', 'number',)
    list_filter = ('building',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('building',)
    search_fields = ('number',)

    def building_link(self, obj=None):
        if obj and obj.building_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_building_change", args=(obj.building_id,)) , escape(obj.building)))
        else: return '-'
    building_link.short_description = _("building")
    building_link.admin_order_field = 'building'

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

class CurriculumInline(admin.TabularInline):
    model = Curriculum
    form = CurriculumForm
    show_change_link = True

@admin.register(GroupStream)
class GroupStreamAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    inlines = [
        CurriculumInline,
    ]
    list_display = ('__str__', 'specialty_link', 'year', 'form_link',)
    list_filter = ('specialty__faculty', YearFilter, 'form',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('specialty', 'form')
    autocomplete_fields = ('specialty',)
    search_fields = (
        'specialty__name', 'specialty__number',
        'specialty__abbreviation', 'year'
    )

    def specialty_link(self, obj=None):
        if obj and obj.specialty_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_specialty_change", args=(obj.specialty_id,)) , escape(obj.specialty)))
        else: return '-'
    specialty_link.short_description = _("specialty")
    specialty_link.admin_order_field = 'specialty'

    def form_link(self, obj=None):
        if obj and obj.form_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_formofstudy_change", args=(obj.form_id,)) , escape(obj.form)))
        else: return '-'
    form_link.short_description = _("form")
    form_link.admin_order_field = 'form'

    def get_search_results(self, request, queryset, search_term):
        filter_q = Q()
        reg = regex.compile(r"^(\p{L}+?)-((\d)((\d)(\p{L}*?)([0-9-]*))?)?$", regex.IGNORECASE)
        st = ""
        mgth = MAX_GROUP_TREE_HEIGHT
        for i in search_term.split(' '):
            if reg.match(i):
                g = reg.search(i)
                filter_dict = {
                    'specialty__abbreviation__exact': g.group(1),
                }
                if g.group(3):
                    y = str(g.group(3))
                    if g.group(5): y += str(g.group(5))
                    filter_dict['year__contains'] = y
                if g.group(6):
                    filter_dict['form__suffix'] = g.group(6)
                filter_q = filter_q | Q(**filter_dict)
            else:
                st += " " + i
        queryset, use_distinct = super().get_search_results(request, queryset, st)
        if filter_q:
            queryset = queryset.filter(filter_q)
        return queryset, use_distinct

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
    show_change_link = True

class GroupStreamYearFilter(YearFilter):
    year_field_path = 'group_stream__'

@admin.register(Group)
class GroupAdmin(AdminWithSelectRelated, MPTTModelAdmin, ImportExportModelAdmin):
    list_display = ('__str__', 'group_stream_link',)
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

    def group_stream_link(self, obj=None):
        if obj and obj.group_stream_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_groupstream_change", args=(obj.group_stream_id,)), escape(obj.group_stream)))
        else: return '-'
    group_stream_link.short_description = _("group stream")
    group_stream_link.admin_order_field = 'group_stream'

    def parent_link(self, obj=None):
        if obj and obj.parent_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_group_change", args=(obj.parent_id,)), escape(obj.parent)))
        else: return '-'
    parent_link.short_description = _("parent node")
    parent_link.admin_order_field = 'parent'

    def get_readonly_fields(self, request, obj=None):
        if obj: return [
            'group_stream_link', 'parent_link', 'group_stream', 'parent',
        ]
        else: return []

    def get_search_results(self, request, queryset, search_term):
        prefix = ''
        filter_q = Q()
        reg = regex.compile(r"^(\p{L}+?)-((\d)((\d)(\p{L}*?)([0-9-]*))?)?$", regex.IGNORECASE)
        st = ""
        mgth = MAX_GROUP_TREE_HEIGHT
        for i in search_term.split(' '):
            if reg.match(i):
                g = reg.search(i)
                filter_dict = {
                    'group_stream__specialty__abbreviation__exact': g.group(1),
                }
                if g.group(3):
                    y = str(g.group(3))
                    if g.group(5): y += str(g.group(5))
                    filter_dict['group_stream__year__contains'] = y
                if g.group(6):
                    filter_dict['group_stream__form__suffix'] = g.group(6)
                elif g.group(7) and g.group(7)[0] == '-':
                    filter_dict['group_stream__form__suffix'] = ''
                filter_qq = Q()
                if g.group(7) and len(g.group(7)) > 1 and g.group(7)[0] == '-':
                    s = []
                    for i in g.group(7)[1:].split('-'):
                        if i: s.append(i)
                        else: break
                    if s:
                        r = mgth - len(s)
                        for i in range(0, r + 1):
                            fd = {
                                '%s__isnull' % ('__parent' * (mgth - i + 1))[2:]: True,
                            }
                            for j in range(0, len(s)):
                                fd['%snumber__exact' % ('parent__' * (mgth - j - i - 1))] = s[j]
                            filter_qq = filter_qq | Q(**fd)
                filter_q = filter_q | Q(filter_qq, **filter_dict)
            else:
                st += " " + i
        queryset, use_distinct = super().get_search_results(request, queryset, st)
        if filter_q:
            queryset = queryset.filter(filter_q)
        p = request.path.find('/autocomplete') != -1
        f = 'filter' in request.GET
        if request.is_ajax() and p and f:
            filter_dict = json.loads(request.GET['filter'])
            queryset = queryset.filter(**filter_dict)
        return queryset, use_distinct

class CurriculumRecordInline(AdminStackedInlineWithSelectRelated):
    model = CurriculumRecord
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
    show_change_link = True

class GroupYearFilter(YearFilter):
    year_field_path = 'group__'

class CurriculumGroupStreamFilter(AutocompleteFilter):
    title = 'Group stream'
    field_name = 'group'

@admin.register(Curriculum)
class CurriculumAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    inlines = [
        CurriculumRecordInline,
    ]
    list_display = ('__str__', 'group_link', 'semester',)
    list_filter = (
        'group__specialty__faculty', GroupYearFilter,
        'group__form', 'semester', CurriculumGroupStreamFilter,
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
        'group__specialty__abbreviation', 'group__year',
    )

    def group_link(self, obj=None):
        if obj and obj.group_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_groupstream_change", args=(obj.group_id,)) , escape(obj.group)))
        else: return '-'
    group_link.short_description = _("group stream")
    group_link.admin_order_field = 'group'

    class Media:
        pass

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

class CurriculumRecordCurriculumGroupFilter(AutocompleteFilter):
    title = _('group stream')
    field_name = 'curriculum__group'

@admin.register(CurriculumRecord)
class CurriculumRecordAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = (
        '__str__', 'group_link', 'get_semester', 'subjects_link',
        'lectures', 'practices', 'laboratory', 'independent_work',
    )
    list_filter = (
        'curriculum__semester',
        CurriculumRecordCurriculumGroupFilter,
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = generate_list_select_related_for_group(
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
    autocomplete_fields = ('curriculum', 'group', 'subjects', )
    search_fields = (
        'curriculum__group__specialty__name',
        'curriculum__group__specialty__number',
        'curriculum__group__specialty__abbreviation',
        'curriculum__group__year',
        'subjects__name',
    )

    def curriculum_link(self, obj=None):
        if obj and obj.curriculum_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_curriculum_change", args=(obj.curriculum_id,)) , escape(obj.curriculum)))
        else: return '-'
    curriculum_link.short_description = _("curriculum")
    curriculum_link.admin_order_field = 'curriculum'

    def group_link(self, obj=None):
        if obj and obj.group_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_group_change", args=(obj.group_id,)) , escape(obj.group)))
        else: return '-'
    group_link.short_description = _("group")
    group_link.admin_order_field = 'group'

    def subjects_link(self, obj=None):
        if obj and obj.subjects.exists():
            s = []
            for i in obj.subjects.all():
                mst = (reverse("admin:timetableapp_subject_change", args=(i.id,)) , escape(i))
                s.append('<a href="%s">%s</a>' % mst)
            return mark_safe(" / ".join(s))
        else: return '-'
    subjects_link.short_description = _("subjects")

    def get_semester(self, obj):
        return obj.curriculum.semester
    get_semester.short_description = _("semester")
    get_semester.admin_order_field = 'curriculum__semester'

    def get_inline_instances(self, request, obj=None):
        if obj:
            return [CurriculumRecordTeacherInline(self.model, self.admin_site)]
        else: return []

    def get_readonly_fields(self, request, obj=None):
        if obj: return [
            'curriculum_link', 'group_link', 'curriculum', 'group',
        ]
        else: return []

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(CurriculumRecordAdmin, self).get_form(request, obj, **kwargs)

    def lookup_allowed(self, key, *args, **kwargs):
        if key  == 'curriculum__group__id__exact':
            return True
        return super(CurriculumRecordAdmin, self).lookup_allowed(key,  *args, **kwargs)

    class Media:
        pass

class TimetableRecordingGroupFilter(AutocompleteFilter):
    title = _('group')
    field_name = 'group'

    def queryset(self, request, queryset):
        if self.value():
            g = Group.objects.filter(pk=self.value()).first()
            args = {
                'group__lft__gte': g.lft,
                'group__rght__lte': g.rght,
            }
            return queryset.filter(**args)

class TimetableRecordingClassroomFilter(AutocompleteFilter):
    title = _('classroom')
    field_name = 'classroom'

class TimetableRecordingTeacherFilter(AutocompleteFilter):
    title = _('teacher')
    field_name = 'teacher'

@admin.register(TimetableRecording)
class TimetableRecordingAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = (
        'group', 'get_semester', 'subjects_link', 'lesson',
        'classroom', 'teacher',
        'start_date', 'end_date',
    )
    list_filter = (
        'record__curriculum__semester',
        TimetableRecordingGroupFilter,
        TimetableRecordingClassroomFilter,
        TimetableRecordingTeacherFilter,
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = generate_list_select_related_for_group(
        'group', 'parent', (
            'group_stream',
            'group_stream__specialty',
            'group_stream__form',
        )
    ) + [
        'record__curriculum',
        'record__curriculum__group__specialty',
        'record__curriculum__group__form',
        'classroom',
        'classroom__building',
        'teacher',
        'teacher__person',
    ]
    autocomplete_fields = ('record', 'group', 'classroom', 'teacher',)

    def get_semester(self, obj):
        return obj.record.curriculum.semester
    get_semester.short_description = _("semester")
    get_semester.admin_order_field = 'record__curriculum__semester'

    def subjects_link(self, obj=None):
        if obj and obj.record.subjects.exists():
            s = []
            for i in obj.record.subjects.all():
                mst = (reverse("admin:timetableapp_subject_change", args=(i.id,)) , escape(i.name))
                s.append('<a href="%s">%s</a>' % mst)
            return mark_safe(" / <br>".join(s))
        else: return '-'
    subjects_link.short_description = _("subjects")

    class Media:
        pass
