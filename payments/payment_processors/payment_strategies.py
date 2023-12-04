from abc import ABC, abstractmethod
# abstract base class for payment strategies


class PaymentStrategy(ABC):

    @abstractmethod
    def process_payment(self, request):
        # method to process payment
        pass
    
    @abstractmethod
    def payment_success(self, request):
        # method to handle success
        pass

    @abstractmethod
    def payment_failure(self, request):
        # method to handle failure
        pass
