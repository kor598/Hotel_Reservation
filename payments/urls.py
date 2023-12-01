from django.urls import path, include
from .views import process_payment
from .payment_processors.paypal_payment_processor import PaypalPaymentProcessor
from .payment_processors.stripe_payment_processor import StripePaymentProcessor

# unique url  name for each payment success or failure
urlpatterns = [
    # Paypal urls
    path('payment/paypal/', PaypalPaymentProcessor.process_payment),
    path('payment-success/paypal/', PaypalPaymentProcessor.payment_success, name='paypal-return'),
    path('payment-cancelled/paypal/', PaypalPaymentProcessor.payment_failure, name='paypal-cancel'),

    # Stripe urls
    path('payment/stripe/', StripePaymentProcessor.process_payment),
    path('payment-success/stripe/', StripePaymentProcessor.payment_success, name='stripe-return'),
    path('payment-cancelled/stripe/', StripePaymentProcessor.payment_failure, name='stripe-cancel'),
    # path('stripe_webhook/', StripePaymentProcessor.stripe_webhook, name='stripe-webhook')
]
