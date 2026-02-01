from django.urls import path, include

urlpatterns = [
    path('members/', include('core.routes.member_routes')),
    path('gyms/', include('core.routes.gym_routes'))
]