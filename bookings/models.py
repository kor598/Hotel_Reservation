from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from loyaltySystem.models import LoyaltySystem
from django_project import settings
from hotel.models import Room

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # gets the right user model
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    points_earned = models.IntegerField(default=0)
    
    # Payment status
    class PaymentStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        PAID = 'Paid', 'Paid'
        FAILED = 'Failed', 'Failed'
        REFUNDED = 'Refunded', 'Refunded'

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    

    def _str_(self):
        return f'{self.user} has booked {self.room} from {self.check_in_date} to {self.check_out_date}'

    # returns the room type
    def get_room_type(self):
        room_types = dict(self.room.ROOM_TYPES)
        room_type = room_types.get(self.room.room_type)
        return room_type

    # calculates nights of stay
    def nights_of_stay(self):
        return (self.check_out_date - self.check_in_date).days  

    # calculates the total price using nights of stay
    def calculate_price(self):
        nights = self.nights_of_stay()
        room_price = self.room.room_price
        total_price = nights * room_price
        
        self.total_price = total_price
        self.save()
        
        return total_price

    # calculates the discount percentage
    def calculate_discount(self, user_points):
        discount_percentage = 0
        if user_points >= 1000:
            max_discount_percentage = 50
            discount_percentage = min((user_points // 1000) * 10, max_discount_percentage)
        return discount_percentage

    # calculates the points earned
    def calculate_points_earned(self):
        
        nights = self.nights_of_stay()
        points_per_night = 100  # Standard tier
        # Update points based on membership tiers
        
        loyalty_details = LoyaltySystem.objects.get(user=self.user)
        membership_tier = loyalty_details.membership_tier
        
        if membership_tier == 'Silver':
            points_per_night = 110
        elif membership_tier == 'Gold':
            points_per_night = 125
        elif membership_tier == 'Diamond':
            points_per_night = 150
        self.points_earned = nights * points_per_night  
        self.save()  
        return nights * points_per_night

    # calculates the price after discount
    def apply_discount(self):
        loyalty_details = LoyaltySystem.objects.get(user=self.user)
        user_points = loyalty_details.total_points
        discount_percentage = self.calculate_discount(user_points)
        price = self.calculate_price()
        
        # Apply discount if applicable
        if discount_percentage > 0:
            discount_amount = (discount_percentage / 100) * price
            discounted_price = price - discount_amount
            price = discounted_price

        return price
    
    # calculates the points deducted
    def calculate_points_deducted(self):
        loyalty_details = LoyaltySystem.objects.get(user=self.user)
        user_points = loyalty_details.total_points
        discount_percentage = self.calculate_discount(user_points)
        points_to_minus = discount_percentage * 100
        loyalty_details.total_points -= points_to_minus
        loyalty_details.save()
        return points_to_minus
        
        # returns the booking url
    def get_cancel_booking_url(self):
        return reverse_lazy('bookings:CancelBookingView', args=[self.pk])
    
    # returns the booking url
    def update_payment_status(self, new_status):
        # Method to update the payment status
        self.payment_status = new_status
        self.save()