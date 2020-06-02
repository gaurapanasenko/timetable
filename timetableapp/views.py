import datetime
import math
from collections import defaultdict
from itertools import accumulate

from django.http import HttpResponse
from django.template.loader import render_to_string

from lesson_field import settings as lesson_settings
from lesson_field.settings import DAY_NAMES, MAX_LESSONS_DAY, SHORT_WEEK_NAMES

from .models import TimeTableRecording, SubGroup, Lesson


DAY_ROWS = 2 * lesson_settings.MAX_LESSONS_DAY
WEEK_ROWS = DAY_ROWS * len(lesson_settings.WORK_DAYS)


def get_row(week, day, lesson):
    return  DAY_ROWS * day + 2 * (lesson - 1) + week + 2

def gen_cell(data, rowspan=1, colspan=1, width="100px"):
    return (rowspan, colspan, data, width)


def lcm(a, b):
    return (a * b) // math.gcd(a, b)


def default_group_data():
    return ({1}, 1)

def accum_groups(elem, acc):
    elem[1]["position"] += acc[1]['max_width']
    return elem

def current_datetime(request, group_stream, semester):
    ttrs = list(TimeTableRecording.objects.filter(
        lesson__subgroup__group__group_stream=group_stream,
        lesson__semester=semester,
    ).select_related(
        'lesson',
        'lesson__subject',
        'lesson__subject__department',
        'lesson__subgroup',
        'lesson__subgroup__group',
        'lesson__subgroup__group__group_stream',
        'lesson__subgroup__group__group_stream__specialty',
        'lesson__subgroup__group__group_stream__form',
    ).order_by(
        'lesson__subgroup__numerator',
        'lesson__subgroup__denominator',
        'lesson__subgroup__group__number',
    ).all())

    group_stream = ttrs[0].lesson.subgroup.group.group_stream
    subgroups = {i.lesson.subgroup for i in ttrs}
    groups = defaultdict(set)
    max_colspan = 1
    for i in subgroups:
        group = i.group
        denominator = i.denominator
        if not group.is_union() and not i.is_union():
            groups[group].add(denominator)
            max_colspan = lcm(max_colspan, denominator)

    data = tuple([] for i in range(WEEK_ROWS + 2))
    posl = list(0 for i in range(WEEK_ROWS + 2))
    group_pos = {v: k for k, v in enumerate(groups.keys())}
    max_max_colspan = len(group_pos) * max_colspan
    LESSON_NAMES = dict(Lesson.LESSON_CHOICES)

    for i in range(2):
        for j in range(3):
            data[i].append(gen_cell(""))
        posl[i] = max_max_colspan

    for group, i in groups.items():
        data[0].append(gen_cell(str(group), 1, max_colspan))
        subgroup = max(i)
        sub_colspan = max_colspan // subgroup
        for j in range(1, subgroup + 1):
            data[1].append(gen_cell(j, 1, sub_colspan))

    for day in lesson_settings.WORK_DAYS:
        data[get_row(0, day, 1)].append(gen_cell(DAY_NAMES[day], DAY_ROWS))
        for lesson in range(1, MAX_LESSONS_DAY + 1):
            data[get_row(0, day, lesson)].append(gen_cell(lesson, 2))
            for week in range(2):
                data[get_row(week, day, lesson)].append(
                    gen_cell(SHORT_WEEK_NAMES[week + 1]))

    for i in ttrs:
        lesson = i.lesson_number
        numerator = i.lesson.subgroup.numerator
        denominator = i.lesson.subgroup.denominator
        group = i.lesson.subgroup.group
        if group.is_union():
            colspan = max_max_colspan
        else:
            colspan = max_colspan // denominator if denominator else max_colspan
        week = lesson.week
        row = get_row(week - 1, lesson.day, lesson.lesson)
        if week == 0b11:
            row -= 2
        out_pos = group_pos[group] * max_colspan if group in group_pos else 0
        inner_pos = max_colspan // denominator * numerator if denominator else 0
        pos = out_pos + inner_pos - 1
        print(out_pos, inner_pos, posl[row], bin(week), max_colspan, denominator, colspan)
        if week == 0b11:
            diff = pos - posl[row]
            if diff > 0:
                if posl[row] == posl[row + 1]:
                    data[row].append(gen_cell("", 2, diff))
                    posl[row] += diff
                    posl[row + 1] += diff
                else:
                    data[row].append(gen_cell("", 1, diff))
                    posl[row] += diff
                    diff2 = pos - posl[row + 1]
                    data[row + 1].append(gen_cell("", 1, diff2))
                    posl[row + 1] += diff2
        else:
            diff = pos - posl[row]
            if diff > 0:
                data[row].append(gen_cell("", 1, diff))
                posl[row] += diff
        lesson_name = LESSON_NAMES[i.lesson.lesson]
        teacher_name = "-"
        if i.teacher:
            teacher_name = i.teacher.person.last_name
        string = "%s (%s) %s %s" % (
            i.lesson.subject, lesson_name, teacher_name,
            i.classroom
        )
        if week == 0b11:
            data[row].append(gen_cell(string, 2, colspan))
            posl[row] += colspan
            posl[row + 1] += colspan
        else:
            data[row].append(gen_cell(string, 1, colspan))
            posl[row] += colspan

    for row in range(len(posl)):
        diff = max_max_colspan - posl[row]
        if diff > 0:
            rows = 1
            if row % 2 == 0 and posl[row] == posl[row + 1]:
                rows = 2
            data[row].append(gen_cell("", rows, diff))
            for i in range(rows):
                posl[row + i] += diff


    return HttpResponse(render_to_string('timetableapp/timetable.html', {
        'data': data,
    }))
