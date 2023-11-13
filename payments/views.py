from django.shortcuts import render
from django.http import HttpResponse
from payment_processors import PaymentProcessorFactory

def process_payment(request, processor_type):
    # Create a Payment Processor depending on the processor type  
    factory = PaymentProcessorFactory()
    processor = factory.create_payment_processor(processor_type)

    # Process the Payment
    processor.processPayment()

    # Return response to the client
    return HttpResponse(f"Payment processed with {processor_type}")