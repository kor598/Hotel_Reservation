from .payment_strategies import PaymentStrategy
from django.views import View
from django.conf import settings
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.shortcuts import render, redirect
# from django.contrib import messages


# concrete strategy for PayPal
class PaypalPaymentProcessor(PaymentStrategy, View):
# add self later
    def process_payment(request):
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '20.00',  # replace with order total later
            'item_name': 'Order 1',  # replace with order number later
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': f'http://{host}{reverse("paypal-ipn")}',
            'return_url': f'http://{host}{reverse("paypal-return")}',
            'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form}
        return render(request, 'payment.html', context)

    def payment_success(request):
        # messages.success(request, 'Your order has been successfully processed')
        return render(request, 'success.html')
        #return redirect(reverse('success'))


    def payment_failure(request):
        # messages.error(request, 'Your order has been cancelled')
        return render(request, 'cancelled.html')
        # return redirect(reverse('cancelled'))

