from payment_processor import PaymentProcessor

class PaypalPaymentProcessor(PaymentProcessor):
    def processPayment(self):
        # paypal process implemeation
        print("Payment processed with Paypal")