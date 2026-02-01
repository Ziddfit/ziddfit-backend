from django.urls import path
from core.views.gym_views import gym_list, gym_detail 

urlpatterns = [
    path('', gym_list, name='gym-list'),
    path('<uuid:gym_id>', gym_detail, name = 'gym-detail')
]