# core/urls.py
from django.urls import path
from core.views.attendance_views import *

urlpatterns = [
    path('gyms/<uuid:gym_id>/attendance/', attendance_list, name='attendance-list'),

    path('gyms/<uuid:gym_id>/attendance/today/', attendance_today, name='attendance-today'),

    path('gyms/<uuid:gym_id>/attendance/stats/', attendance_stats, name='attendance-stats'),

    path('attendance/<uuid:attendance_id>/', attendance_detail, name='attendance-detail'),

    path('attendance/checkin/<uuid:gym_id>/', attendance_checkin, name='attendance-checkin'),
]