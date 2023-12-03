from django.urls import path, include
from .views import process_payment, payment_success, payment_failure
from .payment_processors.paypal_payment_processor import PayPalPaymentProcessor
from .payment_processors.stripe_payment_processor import StripePaymentProcessor


# unique url  name for each payment success or failure
urlpatterns = [
    # Paypal urls
    path('payment/paypal/<int:booking_id>/', process_payment, {'processor_type': 'paypal'}, name='paypal-payment'),
    path('payment-success/paypal/', PayPalPaymentProcessor.as_view(), name='paypal-return'),
    path('payment-cancelled/paypal/', PayPalPaymentProcessor.as_view(), name='paypal-cancel'),
    path('payment-success/<int:booking_id>/', payment_success, name='payment_success'),
    path('payment-failure/<int:booking_id>/', payment_failure, name='payment_failure'),

    # Stripe urls
    path('payment/stripe/<int:booking_id>/', StripePaymentProcessor),
    path('payment-success/stripe/', StripePaymentProcessor, name='stripe-return'),
    path('payment-cancelled/stripe/', StripePaymentProcessor, name='stripe-cancel'),
    # path('stripe_webhook/', StripePaymentProcessor.stripe_webhook, name='stripe-webhook')
]