from django.urls import path, include
from .views import process_payment
from .payment_processors.paypal_payment_processor import PaypalPaymentProcessor
from .payment_processors.stripe_payment_processor import StripePaymentProcessor


# unique url  name for each payment success or failure
urlpatterns = [
    # Paypal urls
    path('payment/paypal/<int:booking_id>/', PaypalPaymentProcessor.as_view(), name='paypal-payment'),    
    path('payment-success/paypal/', PaypalPaymentProcessor.as_view(), name='paypal-return'),
    path('payment-cancelled/paypal/', PaypalPaymentProcessor.as_view(), name='paypal-cancel'),

    # Stripe urls
    path('payment/stripe/<int:booking_id>/', StripePaymentProcessor),
    path('payment-success/stripe/', StripePaymentProcessor, name='stripe-return'),
    path('payment-cancelled/stripe/', StripePaymentProcessor, name='stripe-cancel'),
    # path('stripe_webhook/', StripePaymentProcessor.stripe_webhook, name='stripe-webhook')
]
