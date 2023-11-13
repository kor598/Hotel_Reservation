from django.urls import path
from .views import process_payment

urlpatterns = [
    path('process_payment/<str:processor_type>/', process_payment, name='process_payment'),
]