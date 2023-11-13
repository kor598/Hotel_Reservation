from paypal_payment_processor import PaypalPaymentProcessor
from stripe_payment_processor import StripePaymentProcessor

# Factory class responsible for creating payment processors
class PaymentProcessorFactory: 
    # create a payment processor based on the processor type
    def create_payment_processor(self, processor_type):
        # paypal processor
        if processor_type == "paypal":
            return PaypalPaymentProcessor()
        # stripe processor
        elif processor_type == "stripe":
            return StripePaymentProcessor()
        else:
            return None