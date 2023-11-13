from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .payment_processors.payment_processor_factory import PaymentProcessorFactory


def process_payment(request, processor_type):

    #order_id = request.session.get('order_id')
    #order = get_object_or_404(Order, id=order_id)

    # Create a Payment Processor depending on the processor type  
    factory = PaymentProcessorFactory()
    processor = factory.create_payment_processor(processor_type)

    # Process the Payment
    response = processor.processPayment(request)

    # Return response to the client
    return response