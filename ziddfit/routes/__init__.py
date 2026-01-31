from django.urls import path, include

urlpatterns = [
    path('members/', include('gym_app.routes.member_routes')),
    path('auth/', include('gym_app.routes.user_routes')),
]