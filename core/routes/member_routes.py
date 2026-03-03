from django.urls import path
from core.views.member_views import member_list, member_profile

urlpatterns = [
    path('gyms/<uuid:gym_id>/members/', member_list, name='member-list'),
    path('gyms/<uuid:gym_id>/members/<uuid:memberid>/', member_profile, name='member-profile'),
]