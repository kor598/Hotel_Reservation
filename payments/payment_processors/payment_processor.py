from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def processPayment(self):
        pass