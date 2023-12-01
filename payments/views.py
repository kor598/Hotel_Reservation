from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .payment_processors.paypal_payment_processor import PaypalPaymentProcessor
from .payment_processors.stripe_payment_processor import StripePaymentProcessor

def get_payment_strategy(processor_type):

    # payment strategies available
    payment_strategies = {
        'paypal': PaypalPaymentProcessor,
        'stripe': StripePaymentProcessor,
    }

    return payment_strategies.get(processor_type)

def process_payment(request, processor_type):

    # get the payment strategy selected
    payment_strategy = get_payment_strategy(processor_type)

    # instantiate the strategy
    payment_processor = payment_strategy()

    if payment_strategy:
        payment_processor_instance = payment_strategy()
        return payment_processor_instance.process_payment(request)

    # Handle unsupported payment method
    return render(request, 'error.html', {'error_message': 'Unsupported payment method'})
