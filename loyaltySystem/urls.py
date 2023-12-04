from django.urls import include, path
from .views import loyalty_view


app_name="loyaltySystem"

urlpatterns = [
    path('loyalty/', loyalty_view, name='loyalty_view'),
]
