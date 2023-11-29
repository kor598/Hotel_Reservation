from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from payment_processors.paypal_payment_processor import PaypalPaymentProcessor
from payment_processors.stripe_payment_processor import StripePaymentProcessor

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
    
    if payment_strategy is None:
        # Handle unsupported payment method
        return render(request, 'error_template.html', {'error_message': 'Unsupported payment method'})

    payment_processor = payment_strategy()
    payment_result = payment_processor.process_payment(request)

    if payment_result == 'success':
        return payment_processor.handle_success(request)
    else:
        return payment_processor.handle_failure(request)