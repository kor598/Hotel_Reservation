from django.urls import path, include
from .views import process_payment
from .payment_processors.paypal_payment_processor import PaypalPaymentProcessor
from .payment_processors.stripe_payment_processor import StripePaymentProcessor


urlpatterns = [
    path('payment/', PaypalPaymentProcessor.process_payment),
    path('payment-success/', PaypalPaymentProcessor.payment_success, name='paypal-return'),
    path('payment-cancelled/', PaypalPaymentProcessor.payment_failure, name='paypal-cancel'),
]