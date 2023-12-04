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

    def get(self, request, booking_id):

        payer_id = request.GET.get('PayerID')

        if payer_id:
            # Payment success logic
            return self.payment_success(request, booking_id, payer_id)
        else:
            # Payment failure logic
            return self.payment_failure(request, booking_id)

    def process_payment(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            # Handle the case where the booking is not found
            return render(request, 'booking_not_found.html')

        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': booking.total_price,
            'item_name': f'Booking # {booking.id}',
            'invoice': str(uuid.uuid4()),
            'currency_code': 'EUR',
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(reverse('paypal-success', kwargs={'booking_id': booking.id})),
            'cancel_return': request.build_absolute_uri(reverse('paypal-cancelled', kwargs={'booking_id': booking.id})),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form, 'booking': booking}
        return render(request, 'payment.html', context)
    
    def payment_success(self, request, booking_id, payer_id):

        booking = Booking.objects.get(id=booking_id)

        order = Order.objects.create(
            user=request.user,  # Assuming the user is authenticated
            amount=booking.total_price,
            status='Paid',
            booking=booking,
            payer_id=payer_id,  # Include payer_id in the order
        )

        booking.payment_status = 'Paid'
        booking.save()

        return render(request, 'success.html', {'order': order, 'booking': booking})


    def payment_failure(self, request, booking_id):

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            # Handle the case where the booking is not found
            return render(request, 'booking_not_found.html')

        order = Order.objects.create(
            user=request.user,  # Assuming the user is authenticated
            amount=booking.total_price,
            status='Failed',  # You can set a different status for failed payments
            booking=booking,
        )

        booking.payment_status = 'Failed'
        booking.save()

        # Handle failure within the payment processor
        return render(request, 'cancelled.html', {'order': order, 'booking': booking})
