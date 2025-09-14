from django.urls import path
from .views import InitiatePaymentView, PaystackWebhookView

urlpatterns = [
    path('initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('webhook/', PaystackWebhookView.as_view(), name='paystack-webhook'),
]
