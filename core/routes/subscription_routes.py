from django.urls import path
from core.views.subscription_views import subscription_list, subscription_detail

urlpatterns = [
    path('subscriptions/', subscription_list, name='subscription-list'),
    path('subscriptions/<uuid:pk>/', subscription_detail, name='subscription-detail'),
]
