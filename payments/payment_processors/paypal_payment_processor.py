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
            'amount': str(booking.total_amount),  # Replace with the dynamic total amount
            'item_name': f'Booking #{booking.id}',  # Replace with dynamic booking details
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': f'http://{host}{reverse("paypal-ipn")}',
            'return_url': f'http://{host}{reverse("paypal-return")}',
            'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form}
        return render(request, 'payment.html', context)

    def payment_success(self, request):
        return render(request, 'success.html')

    def payment_failure(self, request):
        return render(request, 'cancelled.html')
