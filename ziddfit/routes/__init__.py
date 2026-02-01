from django.urls import path, include

urlpatterns = [
    path('members/', include('ziddfit.routes.member_routes')),
    path('gyms/', include('ziddfit.routes.gym_routes')),
    path('auth/', include('ziddfit.routes.user_routes')),
]