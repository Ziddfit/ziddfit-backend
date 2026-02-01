from django.urls import path
from ..views.gym_views import gym_list, gym_detail 

urlpatterns = [
    path('/', gym_list, name='gym-list'),
    path('/<int:gym_id>', gym_detail, name = 'gym-detail')
]