from django.urls import path

from . import views

urlpatterns = [
    path('timetable/<int:curriculum>', views.current_datetime),
]
