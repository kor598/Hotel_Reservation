from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .payment_processors.paypal_payment_processor import PayPalPaymentProcessor
from .payment_processors.stripe_payment_processor import StripePaymentProcessor
from bookings.models import Booking

def get_payment_strategy(processor_type):

    # payment strategies available 
    payment_strategies = {
        'paypal': PayPalPaymentProcessor,
        'stripe': StripePaymentProcessor,
    }

    return payment_strategies.get(processor_type)

def process_payment(request, processor_type, booking_id):
    
    # Retrieve booking details based on booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Get the payment strategy selected
    payment_strategy = get_payment_strategy(processor_type)

    # Check if the payment strategy is available
    if payment_strategy:
        # Instantiate the payment strategy
        payment_processor = payment_strategy()
        # Process the payment with booking_id
        return payment_processor.process_payment(request, booking_id)

    return render(request, 'error.html', {'error_message': 'Payment method not found'})
