from django.urls import include, path
from .views import loyalty_view


app_name="loyaltySystem"

# URL patterns for the loyaltySystem app
urlpatterns = [
    path('loyalty/', loyalty_view, name='loyalty_view'),
]
