from .payment_processor import PaymentProcessor

class StripePaymentProcessor(PaymentProcessor):
    def processPayment(self):
        # stripe process implemeation
        print("Payment processed with Stripe")