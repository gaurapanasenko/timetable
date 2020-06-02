from django.urls import path

from . import views

urlpatterns = [
    path('timetable/<int:group_stream>/<int:semester>', views.current_datetime),
]
