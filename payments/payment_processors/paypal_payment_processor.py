from .payment_strategies import PaymentStrategy
from django.views import View
from django.conf import settings
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.shortcuts import render, redirect

# concrete strategy for PayPal
class PaypalPaymentProcessor(PaymentStrategy, View):

    def process_payment(self, request, booking):
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': str(booking.total_price),  # replace with actual amount
            'item_name': f'Booking {booking.id}',  # replace with relevant information
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': request.build_absolute_uri(reverse('payment_success')),
            'cancel_return': request.build_absolute_uri(reverse('payment_failure')),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form}
        return render(request, 'payment.html', context)

    def payment_success(self, request):
        return render(request, 'success.html')

    def payment_failure(self, request):
        return render(request, 'cancelled.html')
