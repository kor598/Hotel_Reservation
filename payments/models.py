from django.db import models
from accounts.models import User
from bookings.models import Booking
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    payer_id = models.CharField(max_length=255, null=True, blank=True)  # Add this line

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.timestamp}"
