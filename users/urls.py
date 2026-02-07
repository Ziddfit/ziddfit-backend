from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.user_Profile, name='get_current_user'),
]