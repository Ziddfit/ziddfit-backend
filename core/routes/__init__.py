from django.urls import path, include

urlpatterns = [
    path('members/', include('core.routes.member_routes')),
    path('gyms/', include('core.routes.gym_routes'))
    path('attendance/', include('core.roues.attendance_routes'))
]