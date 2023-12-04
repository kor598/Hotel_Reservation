from bookings.models import Booking
from .payment_strategies import PaymentStrategy
from django.views import View
from django.conf import settings
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.shortcuts import render, redirect
from payments.models import Order

# concrete strategy for PayPal

class PayPalPaymentProcessor(PaymentStrategy, View):

    # get method to process payment
    def get(self, request, booking_id):
        # get payer_id from the request
        payer_id = request.GET.get('PayerID')

        if payer_id:
            # Payment success logic
            return self.payment_success(request, booking_id, payer_id)
        else:
            # Payment failure logic
            return self.payment_failure(request, booking_id)

    # payemment process method for paypal
    def process_payment(self, request, booking_id):
        # get booking id form booking object
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return render(request, 'error.html',  {'error_message': 'Booking not found'})

        # get host from request
        host = request.get_host()

        # create paypal dictionary with required fields
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL, # business receiver email from settings
            'amount': booking.total_price, # get total price from booking object
            'item_name': f'Booking # {booking.id}', # get booking id from booking object
            'invoice': str(uuid.uuid4()), # generate unique invoice id
            'currency_code': 'EUR', 
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
             # set return url for paypal if payment successfull
            'return_url': request.build_absolute_uri(reverse('paypal-success', kwargs={'booking_id': booking.id})),
             # set cancel url for paypal if payment cancelled
            'cancel_return': request.build_absolute_uri(reverse('paypal-cancelled', kwargs={'booking_id': booking.id})),
        }

        # create paypal form with paypal dictionary
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form, 'booking': booking}

        return render(request, 'payment.html', context)
    
    # payment success method for paypal
    def payment_success(self, request, booking_id, payer_id):

        # get booking object from booking id
        booking = Booking.objects.get(id=booking_id)

        # create order object with booking object
        order = Order.objects.create(
            user=request.user,  # Assuming the user is authenticated
            amount=booking.total_price,
            status='Paid',
            booking=booking,
            payer_id=payer_id,  
        )
        
        # update booking payment status to paid
        booking.payment_status = 'Paid'
        booking.save()

        return render(request, 'success.html', {'order': order, 'booking': booking})

    # payment failure method for paypal
    def payment_failure(self, request, booking_id):

        # get booking object from booking id
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:

            return render(request, 'error.html', {'error_message': 'Booking not found'})

        # create order object with booking object
        order = Order.objects.create(
            user=request.user,  
            amount=booking.total_price,
            status='Failed',  
            booking=booking,
        )

        # update booking payment status to failed
        booking.payment_status = 'Failed'
        booking.save()

        # render cancelled.html with order and booking object to disply order information
        return render(request, 'cancelled.html', {'order': order, 'booking': booking})
