from django.urls import path
from core.views.gym_staff import staff_list, staff_detail


urlpatterns = [
    path('gym-staff/', staff_list, name='staff-list'),
    path('gym-staff/<uuid:pk>/', staff_detail, name='staff-detail'),
]
