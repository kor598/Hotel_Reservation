from .payment_strategies import PaymentStrategy


# concrete strategy for Stripe
class StripePaymentProcessor(PaymentStrategy):

    def process_payment(self):
        # stripe process implemeation
        print("Payment processed with Stripe")

    def payment_success(self, request):
        print("Payment successfuly processed with Stripe")

    def payment_failure(self, request):
        print("Payment failed to process with Stripe")

    