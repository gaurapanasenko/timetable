import datetime

from django.http import HttpResponse
from django.template.loader import render_to_string

from lesson_field.models import LessonField

from .models import Curriculum

def current_datetime(request, curriculum):
    c = Curriculum.objects.get(pk=curriculum)
    crs = c.curriculumrecord_set.all()
    for i in crs:
        print(vars(i.timetablerecording_set.all()))
    return HttpResponse(render_to_string('timetableapp/timetable.html', {
        'curriculum': c,
        'lesson_field': LessonField
    }))
