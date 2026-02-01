from django.urls import path
from ..views.member_views import member_list 

urlpatterns = [
    path('', member_list, name='member-list'),
]