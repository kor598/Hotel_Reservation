from django.urls import path
from .views import process_payment

urlpatterns = [
    path('<str:processor_type>/', process_payment, name='process_payment'),
    path('success/', process_payment, name='payment_success'),
    path('cancelled/', process_payment, name='payment_cancelled'),
]