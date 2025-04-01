from django.urls import path
from .views import (
    login_view,
    get_subjects,
    get_students,
    mark_attendance,
    get_attendance
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('subjects/', get_subjects, name='get_subjects'),
    path('students/', get_students, name='get_students'),
    path('attendance/mark/', mark_attendance, name='mark_attendance'),
    path('attendance/get/', get_attendance, name='get_attendance'),
]
