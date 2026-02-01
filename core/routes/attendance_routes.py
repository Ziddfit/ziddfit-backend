from django.urls import path
from core.views.attendance_views import attendance_list, attendance_detail

urlpatterns = [
    path('', attendance_list, name='attendance-list'),
    path('<uuid:attendance_id>/', attendance_detail, name='attendance-detail'),
]
