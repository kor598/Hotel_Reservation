from django.urls import path
from .views import process_payment
from .payment_processors.paypal_payment_processor import PaypalPaymentProcessor
from .payment_processors.payment_processor_factory import PaymentProcessorFactory
from .payment_processors.stripe_payment_processor import StripePaymentProcessor

urlpatterns = [
    path('process_payment/<str:processor_type>/', process_payment, name='paypal-ipn'),
    path('paypal_return/',process_payment, name='payment-return'),
    path('paypal_cancel/',process_payment, name='payment-cancelled'),
]