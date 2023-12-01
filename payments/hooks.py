from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.dispatch import receiver
from models import Order

#
@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:

        Order.objects.create()


@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:

        Order.objects.create()
