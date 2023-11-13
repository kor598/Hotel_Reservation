from .payment_processor import PaymentProcessor
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import uuid



class PaypalPaymentProcessor(PaymentProcessor):
    def processPayment(self, request):
        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '20.00', # replqce with order total later
            'item_name': 'Order 1', # replace with order number later
            'invoice': str(uuid.uuid4()),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host,reverse('payment-return')),
            'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context = {'form': form}
        return render(request, 'payment.html', context)
    
    def paypal_return(self, request):
        messages.success(request, 'Your payment was successful')
        return redirect('process_payment', processor_type='paypal')

    def paypal_cancel(self, request):
        messages.error(request, 'Your order has been cancelled')
        return redirect('process_payment', processor_type='paypal')
