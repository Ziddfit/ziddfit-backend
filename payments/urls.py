from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.CreateSubscriptionView.as_view(), name='create_subscription'),
    path('webhook/', views.RazorpayWebhookView.as_view(), name='razorpay_webhook'),
]