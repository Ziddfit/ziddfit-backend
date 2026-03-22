from django.urls import path
from core.views.gym_views import gym_list, gym_detail 
from core.views.memberSchema_views import member_schema_list, member_schema_detail

urlpatterns = [
    path('', gym_list, name='gym-list'),
    path('<uuid:gym_id>', gym_detail, name = 'gym-detail'),
    path('<uuid:gym_id>/member-schema', member_schema_list, name = 'extra_schema_list' ),
    path('<uuid:gym_id>/member-schema-detail/<uuid:field_id>', member_schema_detail, name = 'extra_schema_detail')
]