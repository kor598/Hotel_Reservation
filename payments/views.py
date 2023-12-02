from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .payment_processors.paypal_payment_processor import PaypalPaymentProcessor
from .payment_processors.stripe_payment_processor import StripePaymentProcessor
from bookings.models import Booking

def get_payment_strategy(processor_type):

    # payment strategies available
    payment_strategies = {
        'paypal': PaypalPaymentProcessor,
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
        payment_processor = payment_strategy()

        # Process payment with booking details
        return payment_processor.process_payment(request, booking)
    # Handle unsupported payment method
    return render(request, 'error.html', {'error_message': 'Payment method not found'})

def payment_success(request):
    
    booking_id = request.GET.get('booking_id')  # Retrieve booking ID from request
    booking = Booking.objects.get(pk=booking_id)  # Fetch the corresponding booking object
    booking.payment_status = 'Paid'
    booking.save()

    # You can render a success page or message to the user
    return render(request, 'success.html')

def payment_failure(request):
    
    booking_id = request.GET.get('booking_id')  # Retrieve booking ID from request
    booking = Booking.objects.get(pk=booking_id)  # Fetch the corresponding booking object
    booking.payment_status = 'Paid'
    booking.save()

    # You can render a success page or message to the user
    return render(request, 'failure.html')