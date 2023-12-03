from .payment_strategies import PaymentStrategy
from django.views import View
from django.conf import settings
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.shortcuts import render, redirect
from models import Order

# concrete strategy for PayPal
class PayPalPaymentProcessor(PaymentStrategy, View):

    def process_payment(self, request, booking):
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': booking.total_price, 
            'item_name': f'Booking # {booking.id}',  
            'invoice': str(uuid.uuid4()),
            'currency_code': 'EUR',
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(reverse('payment_success')),
            'cancel_return': request.build_absolute_uri(reverse('payment_failure')),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form}
        return render(request, 'payment.html', context)

    def payment_success(self, request,booking):
        order = Order.objects.create(
            user=request.user,  # Assuming the user is authenticated
            amount=booking.total_price,
            status='Paid',
            booking=booking,
        )

        # Update booking payment status if needed
        booking.payment_status = 'Paid'
        booking.save()

        return render(request, 'success.html')

    def payment_failure(self, request, booking):
        
        order = Order.objects.create(
            user=request.user,  # Assuming the user is authenticated
            amount=booking.total_price,
            status='Failed',  # You can set a different status for failed payments
            booking=booking,
        )

        # Update booking payment status if needed
        booking.payment_status = 'Failed'
        booking.save()

        # Handle failure within the payment processor
        return render(request, 'cancelled.html', {'order': order})
