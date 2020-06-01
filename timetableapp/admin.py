# pylint: disable=R0201
import json
import regex

from django.utils.translation import ugettext_lazy as _
# from django.shortcuts import (
    # render,
    # redirect,
# )
# from django.http import HttpResponse
from django.contrib import admin
from django.urls import (
    # path,
    reverse,
)
from django.db.models import Q
from django.template.defaultfilters import escape
from django.utils.safestring import mark_safe

from import_export.admin import ImportExportModelAdmin
# from mptt.admin import MPTTModelAdmin
# from mptt.forms import TreeNodeChoiceField
from django_improvements.admin import (
    # AdminBaseWithSelectRelated,
    # AdminInlineWithSelectRelated,
    # AdminStackedInlineWithSelectRelated,
    AdminWithSelectRelated,
    # FilterWithSelectRelated,
)
from admin_auto_filters.filters import AutocompleteFilter

from timetableapp.settings import (
    LIST_PER_PAGE, current_year, START_YEAR,
)

from timetableapp.models import (
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
    SubGroup,
    Building,
    Classroom,
    Curriculum,
    CurriculumRecordingTimings,
    Lesson,
    TimeTableRecording,
)

from timetableapp.forms import (
    FormOfStudySemesterFormset,
    CurriculumForm,
)

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
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_faculty_change", args=(obj.faculty_id,)), escape(obj.faculty)))
        return '-'
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
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_department_change", args=(obj.department_id,)), escape(obj.department)))
        return '-'
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
    autocomplete_fields = ('person', 'department',)
    search_fields = (
        'person__first_name', 'person__middle_name',
        'person__last_name',
        'department__name',
        'department__abbreviation',
    )

    def person_link(self, obj=None):
        if obj and obj.person_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_person_change", args=(obj.person_id,)), escape(obj.person)))
        return '-'
    person_link.short_description = _("person")
    person_link.admin_order_field = 'person'

    def department_link(self, obj=None):
        if obj and obj.department_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_department_change", args=(obj.department_id,)), escape(obj.department)))
        return '-'
    department_link.short_description = _("department")
    department_link.admin_order_field = 'department'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        have_path = request.path.find('/autocomplete') != -1
        filt = 'filter' in request.GET
        if request.is_ajax() and have_path and filt:
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
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_faculty_change", args=(obj.faculty_id,)), escape(obj.faculty)))
        return '-'
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
    search_fields = ('building', 'number',)

    def building_link(self, obj=None):
        if obj and obj.building_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_building_change", args=(obj.building_id,)), escape(obj.building)))
        return '-'
    building_link.short_description = _("building")
    building_link.admin_order_field = 'building'

class FormOfStudySemesterInline(admin.TabularInline):
    model = FormOfStudySemester
    formset = FormOfStudySemesterFormset

@admin.register(FormOfStudy)
class FormOfStudyAdmin(ImportExportModelAdmin):
    inlines = [FormOfStudySemesterInline, GroupStreamInline, ]
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
                    field_path = self.year_field_path
                    args = {
                        '%syear__gte' % field_path: int(years[0]),
                        '%syear__lte' % field_path: int(years[1]),
                    }
                    return queryset.filter(**args)
                except ValueError:
                    pass
        return None

class CurriculumInline(admin.TabularInline):
    model = Curriculum
    form = CurriculumForm
    show_change_link = True

class GroupInline(admin.TabularInline):
    model = Group
    show_change_link = True

@admin.register(GroupStream)
class GroupStreamAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    inlines = (
        CurriculumInline, GroupInline,
    )
    list_display = ('__str__', 'specialty_link', 'year', 'form_link',)
    list_filter = ('specialty__faculty', YearFilter, 'form',)
    list_per_page = LIST_PER_PAGE
    list_select_related = ('specialty', 'form')
    autocomplete_fields = ('specialty', 'form')
    search_fields = (
        'specialty__name', 'specialty__number',
        'specialty__abbreviation', 'year'
    )

    def specialty_link(self, obj=None):
        if obj and obj.specialty_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_specialty_change", args=(obj.specialty_id,)), escape(obj.specialty)))
        return '-'
    specialty_link.short_description = _("specialty")
    specialty_link.admin_order_field = 'specialty'

    def form_link(self, obj=None):
        if obj and obj.form_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_formofstudy_change", args=(obj.form_id,)), escape(obj.form)))
        return '-'
    form_link.short_description = _("form")
    form_link.admin_order_field = 'form'

    def get_search_results(self, request, queryset, search_term):
        filter_q = Q()
        reg = regex.compile(r"^(\p{L}+?)-((\d)((\d)(\p{L}*?)([0-9-]*))?)?$", regex.IGNORECASE)
        tail = ""
        for i in search_term.split(' '):
            if reg.match(i):
                group = reg.search(i)
                filter_dict = {
                    'specialty__abbreviation__exact': group.group(1),
                }
                if group.group(3):
                    year = str(group.group(3))
                    if group.group(5):
                        year += str(group.group(5))
                    filter_dict['year__contains'] = year
                if group.group(6):
                    filter_dict['form__suffix'] = group.group(6)
                filter_q = filter_q | Q(**filter_dict)
            else:
                tail += " " + i
        queryset, use_distinct = super().get_search_results(request, queryset, tail)
        if filter_q:
            queryset = queryset.filter(filter_q)
        return queryset, use_distinct

class GroupStreamYearFilter(YearFilter):
    year_field_path = 'group_stream__'

class SubGroupInline(admin.TabularInline):
    model = SubGroup
    show_change_link = True

class CurriculumRecordingTimingsInline(admin.StackedInline):
    model = CurriculumRecordingTimings
    show_change_link = True

@admin.register(Group)
class GroupAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('__str__', 'group_stream_link',)
    inlines = (SubGroupInline, CurriculumRecordingTimingsInline)
    list_filter = (
        'group_stream__specialty__faculty', GroupStreamYearFilter,
        'group_stream__form',
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = (
        'group_stream',
        'group_stream__specialty',
        'group_stream__form',
    )
    autocomplete_fields = ('group_stream',)
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
        return '-'
    group_stream_link.short_description = _("group stream")
    group_stream_link.admin_order_field = 'group_stream'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('group_stream_link', )
        return tuple()

    def get_search_results(self, request, queryset, search_term):
        filter_q = Q()
        for i in search_term.split(' '):
            for j in i.split('-'):
                if j:
                    filter_qq = (
                        Q(group_stream__specialty__abbreviation__icontains=j) |
                        Q(group_stream__form__suffix__icontains=j) |
                        Q(group_stream__year__icontains=j) |
                        Q(number__icontains=j)
                    )
                    filter_q = (
                        filter_q & filter_qq
                    )
        queryset, use_distinct = super().get_search_results(request, queryset, "")
        if filter_q:
            queryset = queryset.filter(filter_q)
        have_path = request.path.find('/autocomplete') != -1
        filt = 'filter' in request.GET
        if request.is_ajax() and have_path and filt:
            filter_dict = json.loads(request.GET['filter'])
            queryset = queryset.filter(**filter_dict)
        return queryset, use_distinct

class LessonInline(admin.StackedInline):
    model = Lesson
    show_change_link = True

class GroupGroupStreamYearFilter(YearFilter):
    year_field_path = 'group__group_stream__'

@admin.register(SubGroup)
class SubGroupAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('__str__', 'group_link', 'group_group_stream_link',)
    inlines = (LessonInline,)
    list_filter = (
        'group__group_stream__specialty__faculty',
        GroupGroupStreamYearFilter,
        'group__group_stream__form',
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = (
        'group__group_stream',
        'group__group_stream__specialty',
        'group__group_stream__form',
    )
    autocomplete_fields = ('group',)
    search_fields = (
        'group__group_stream__specialty__name',
        'group__group_stream__specialty__number',
        'group__group_stream__specialty__abbreviation',
        'group__group_stream__year',
        'group__number',
    )

    def group_group_stream_link(self, obj=None):
        if obj and obj.group.group_stream_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_groupstream_change", args=(obj.group.group_stream_id,)), escape(obj.group.group_stream)))
        return '-'
    group_group_stream_link.short_description = _("group stream")
    group_group_stream_link.admin_order_field = 'group__group_stream'

    def group_link(self, obj=None):
        if obj and obj.group_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_group_change", args=(obj.group_id,)), escape(obj.group)))
        return '-'
    group_link.short_description = _("group")
    group_link.admin_order_field = 'group'


class GroupYearFilter(YearFilter):
    year_field_path = 'group__'

class CurriculumGroupStreamFilter(AutocompleteFilter):
    title = 'Group stream'
    field_name = 'group_stream'

@admin.register(Curriculum)
class CurriculumAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = ('__str__', 'group_stream_link', 'semester',)
    list_filter = (
        'group_stream__specialty__faculty', GroupYearFilter,
        'group_stream__form', 'semester', CurriculumGroupStreamFilter,
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = [
        'group_stream',
        'group_stream__specialty',
        'group_stream__form',
    ]
    autocomplete_fields = ('group_stream',)
    search_fields = (
        'group_stream__specialty__name', 'group_stream__specialty__number',
        'group_stream__specialty__abbreviation', 'group_stream__year',
    )

    def group_stream_link(self, obj=None):
        if obj and obj.group_stream_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_groupstream_change", args=(obj.group_stream_id,)), escape(obj.group_stream)))
        return '-'
    group_stream_link.short_description = _("group stream")
    group_stream_link.admin_order_field = 'group_stream'

    class Media:
        pass


@admin.register(CurriculumRecordingTimings)
class CurriculumRecordingTimingsAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = (
        '__str__', 'group_link', 'semester', 'subjects_list', 'lectures',
        'practices', 'laboratory', 'independent_work',
    )
    list_filter = (
        'group__group_stream__specialty__faculty', GroupGroupStreamYearFilter,
        'group__group_stream__form', 'semester',
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = (
        'group__group_stream',
        'group__group_stream__specialty',
        'group__group_stream__form',
    )
    autocomplete_fields = ('group',)
    search_fields = (
        'group__group_stream__specialty__name',
        'group__group_stream__specialty__number',
        'group__group_stream__specialty__abbreviation',
        'group__group_stream__year',
        'group__number',
        'semester',
    )

    def subjects_list(self, obj=None):
        if obj:
            return obj.get_subject_name()
        return '-'
    subjects_list.short_description = _("subjects")
    subjects_list.admin_order_field = 'subjects'

    def group_link(self, obj=None):
        if obj and obj.group_id:
            return mark_safe('<a href="%s">%s</a>' % (reverse("admin:timetableapp_group_change", args=(obj.group_id,)), escape(obj.group)))
        return '-'
    group_link.short_description = _("group")
    group_link.admin_order_field = 'group'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('group_link', )
        return tuple()


class TeacherFilter(AutocompleteFilter):
    title = 'Teacher'
    field_name = 'teacher'


@admin.register(Lesson)
class LessonAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = (
        'pk', 'subgroup', 'semester', 'subject', 'lesson', 'teacher',
    )
    list_filter = (
        'subgroup__group__group_stream__specialty__faculty',
        'subgroup__group__group_stream__form',
        'semester', 'lesson', TeacherFilter
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = (
        'subject',
        'subgroup',
        'subgroup__group',
        'subgroup__group__group_stream',
        'subgroup__group__group_stream__specialty',
        'subgroup__group__group_stream__form',
    )
    autocomplete_fields = ('subgroup',)
    search_fields = (
        'subgroup__group__group_stream__specialty__name',
        'subgroup__group__group_stream__specialty__number',
        'subgroup__group__group_stream__specialty__abbreviation',
        'subgroup__group__group_stream__year',
        'subgroup__group__number',
    )

    class Media:
        pass


class CurriculumRecordCurriculumGroupFilter(AutocompleteFilter):
    title = _('group stream')
    field_name = 'curriculum__group'


class TimeTableRecordingLessonFilter(AutocompleteFilter):
    title = _('lesson')
    field_name = 'lesson'


class TimeTableRecordingSubGroupFilter(AutocompleteFilter):
    title = _('subgroup')
    field_name = 'lesson__subgroup'

    def queryset(self, request, queryset):
        if self.value():
            queryset = SubGroup.objects.filter(pk=self.value())
            subgroup = queryset.first()
            if subgroup.is_union():
                queryset = SubGroup.objects.filter(group=subgroup.group)
            return queryset
        return None

class TimeTableRecordingClassroomFilter(AutocompleteFilter):
    title = _('classroom')
    field_name = 'classroom'

class TimeTableRecordingTeacherFilter(AutocompleteFilter):
    title = _('teacher')
    field_name = 'teacher'

@admin.register(TimeTableRecording)
class TimeTableRecordingAdmin(AdminWithSelectRelated, ImportExportModelAdmin):
    list_display = (
        'pk', 'get_semester', 'subjects_link', 'lesson_link',
        'classroom', 'teacher',
        'start_date', 'end_date',
    )
    list_filter = (
        TimeTableRecordingLessonFilter,
        TimeTableRecordingSubGroupFilter,
        TimeTableRecordingClassroomFilter,
        TimeTableRecordingTeacherFilter,
        'lesson__semester',
    )
    list_per_page = LIST_PER_PAGE
    list_select_related = (
        'lesson',
        'lesson__subgroup',
        'lesson__subgroup__group',
        'lesson__subgroup__group__group_stream',
        'lesson__subgroup__group__group_stream__specialty',
        'lesson__subgroup__group__group_stream__specialty__faculty',
        'classroom',
        'classroom__building',
        'teacher',
        'teacher__person',
    )
    autocomplete_fields = ('classroom', 'teacher',)

    def get_semester(self, obj):
        return obj.lesson.semester
    get_semester.short_description = _("semester")
    get_semester.admin_order_field = 'lesson__semester'

    def subjects_link(self, obj=None):
        if obj and obj.lesson.subject_id:
            subject = obj.lesson.subject
            return mark_safe('<a href="%s">%s</a>' % (
                reverse("admin:timetableapp_subject_change", args=(subject.pk,)),
                escape(subject.name),
            ))
        return '-'
    subjects_link.short_description = _("subject")
    subjects_link.admin_order_field = 'lesson__subject'

    def lesson_link(self, obj=None):
        if obj and obj.lesson_id:
            lesson = obj.lesson
            return mark_safe('<a href="%s">%s</a>' % (
                reverse("admin:timetableapp_lesson_change", args=(lesson.pk,)),
                escape(str(lesson)),
            ))
        return '-'
    lesson_link.short_description = _("lesson")
    lesson_link.admin_order_field = 'lesson'

    class Media:
        pass
