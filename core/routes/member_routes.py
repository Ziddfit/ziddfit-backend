from django.urls import path
from core.views.member_views import member_list, member_profile

urlpatterns = [
    path('', member_list, name='member-list'),
    path('<uuid : memberid>/', member_profile, name = 'member-profile')
]