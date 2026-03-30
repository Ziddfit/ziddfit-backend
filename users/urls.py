from django.urls import path
from .authentication import GoogleAuthView, TokenRefreshView, LogoutView
from .views import user_profile, upload_profile_pic

urlpatterns = [
    # --- auth ---
    path('auth/google/',        GoogleAuthView.as_view(),   name='google-auth'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/logout/',        LogoutView.as_view(),       name='logout'),

    # --- profile ---
    path('user/profile/',       user_profile,               name='user-profile'),
    path('user/profile-pic/',   upload_profile_pic,         name='upload-profile-pic'),
]