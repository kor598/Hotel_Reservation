from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from accounts.models import User
#from django.contrib.auth.models import User

from hotel.models import Room

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in_date} to {self.check_out_date}'

    def get_room_type(self):
        room_types = dict(self.room.ROOM_TYPES)
        room_type = room_types.get(self.room.room_type)
        return room_type

    def nights_of_stay(self):
        return (self.check_out_date - self.check_in_date).days  # Calculate nights of stay

    def calculate_price(self):
        nights = self.nights_of_stay()
        room_price = self.room.price
        total_price = nights * room_price
        return total_price

    def calculate_discount(self, user_points):
        discount_percentage = 0
        if user_points >= 1000:
            max_discount_percentage = 50
            discount_percentage = min((user_points // 1000) * 10, max_discount_percentage)
        return discount_percentage

    def calculate_points_earned(self):
        nights = self.nights_of_stay()
        points_per_night = 100  # Standard tier
        # Update points based on membership tiers
        # currently stored as user.membership_tier. CHANGE WHEN RAJAT IS DONE
        if self.user.membership_tier == 'Silver':
            points_per_night = 110
        elif self.user.membership_tier == 'Gold':
            points_per_night = 125
        elif self.user.membership_tier == 'Diamond':
            points_per_night = 150
        return nights * points_per_night

    def update_user_points(self):
        points_earned = self.calculate_points_earned()
        # Update user's points based on the points earned from the booking
        self.user.points += points_earned
        self.user.save()

    def apply_discount(self):
        user_points = self.user.points
        discount_percentage = self.calculate_discount(user_points)
        price = self.calculate_price()

        # Apply discount if applicable
        if discount_percentage > 0:
            discount_amount = (discount_percentage / 100) * price
            discounted_price = price - discount_amount
            return discounted_price
        return price

    def get_cancel_booking_url(self):
        return reverse_lazy('bookings:CancelBookingView', args=[self.pk])