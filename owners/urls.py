from django.urls import path
from . import views

urlpatterns = [
    path('ownerprofile/', views.owner_profile, name='owner-profile'),
]