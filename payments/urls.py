from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.create_subscription, name='create_subscription'),
    path('webhook/', views.razorpay_webhook, name='razorpay_webhook'),
]