from django.urls import path, include

urlpatterns = [
    path('', include('core.routes.member_routes')),
    path('gyms/', include('core.routes.gym_routes')),
    path('', include('core.routes.attendance_routes')),
    path('', include('core.routes.ledger_routes')),
    path('', include('core.routes.subscription_routes')),
    path('', include('core.routes.gym_staff_routes')),
]