from .paypal_payment_processor import PaypalPaymentProcessor
from .stripe_payment_processor import StripePaymentProcessor
# Factory class responsible for creating payment processors
class PaymentProcessorFactory: 
    def create_payment_processor(self, processor_type):
        if processor_type == "paypal":
            return PaypalPaymentProcessor()
        elif processor_type == "stripe":
            return StripePaymentProcessor()
        else:
            return None