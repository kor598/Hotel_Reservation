from abc import ABC, abstractmethod

class PaymentStrategy(ABC):

    @abstractmethod
    def processPayment(self, request):
        pass
    
    @abstractmethod
    def payment_success(self, request):
        pass

    @abstractmethod
    def payment_failure(self, request):
        pass
