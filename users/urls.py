from django.urls import path
from . import views
from .authentication import GoogleAuthView, TokenRefreshView, LogoutView

urlpatterns = [
    path('me/', views.user_Profile, name='get_current_user'),
    path('auth/google/owner/', GoogleAuthView.as_view(), {'role': 'owner'}),
    path('auth/google/', GoogleAuthView.as_view(), {'role': 'member'}),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
]