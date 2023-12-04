from django.urls import path, include
from .views import process_payment
from .payment_processors.paypal_payment_processor import PayPalPaymentProcessor
from .payment_processors.stripe_payment_processor import StripePaymentProcessor


# unique url  name for each payment success or failure
urlpatterns = [
    
    # Paypal urls
    path('payment/paypal/<int:booking_id>/', process_payment, {'processor_type': 'paypal'}, name='paypal-payment'),
    path('payment-success/paypal/<int:booking_id>/', PayPalPaymentProcessor.as_view(), name='paypal-success'),
    path('payment-cancelled/paypal/<int:booking_id>/', PayPalPaymentProcessor.as_view(), name='paypal-cancelled'),
    

    # path('payment-success/', payment_success, name='payment_success'),
    # path('payment-failure/', payment_failure, name='payment_failure'),

    # Stripe urls
    path('payment/stripe/<int:booking_id>/', StripePaymentProcessor),
    path('payment-success/stripe/', StripePaymentProcessor, name='stripe-return'),
    path('payment-cancelled/stripe/', StripePaymentProcessor, name='stripe-cancel'),
    # path('stripe_webhook/', StripePaymentProcessor.stripe_webhook, name='stripe-webhook')
]