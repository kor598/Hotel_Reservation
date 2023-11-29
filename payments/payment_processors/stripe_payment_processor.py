from .payment_strategies import PaymentStrategy

class StripePaymentProcessor(PaymentStrategy):
    def processPayment(self):
        # stripe process implemeation
        print("Payment processed with Stripe")