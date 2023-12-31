from django.db import models
from datetime import datetime, timedelta, timezone
from accounts.models import User
from django.utils import timezone

# Custom manager for LoyaltySystem model
class LoyaltySystemManager(models.Manager):
    pass

# LoyaltySystem model representing loyalty information for users
class LoyaltySystem(models.Model):
    # One-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_points = models.IntegerField(default=0)
    membership_tier = models.CharField(max_length=50, default="Standard")
    last_checkin_date = models.DateTimeField(auto_now_add=True)
    
    # Custom manager for LoyaltySystem model
    objects = LoyaltySystemManager()

    # Method to update the membership tier based on total nights stayed
    def update_membership_tier(self):
        # Calculate the date 366 days ago from today
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=366)
        
        # Query the Booking model for relevant bookings
        from bookings.models import Booking
        relevant_bookings = Booking.objects.filter(
            user=self.user,
            check_in_date__gte=start_date,
            check_out_date__lte=end_date
        )
        
        # Calculate the total number of nights stayed
        total_nights = sum(booking.nights_of_stay() for booking in relevant_bookings)

        # Update membership tier based on total nights stayed
        if total_nights >= 100:
            self.membership_tier = "Diamond"
        elif total_nights >= 50:
            self.membership_tier = "Gold"
        elif total_nights >= 20:
            self.membership_tier = "Silver"
        elif total_nights < 20:
            self.membership_tier = "Standard"
            
        self.save()
        
# Subclasses representing different guest types, inheriting from LoyaltySystem
class StandardGuest(LoyaltySystem):
    loyaltysystem_ptr = models.OneToOneField(LoyaltySystem, on_delete=models.CASCADE, parent_link=True, default=0)

    

class SilverGuest(LoyaltySystem):
    loyaltysystem_ptr = models.OneToOneField(LoyaltySystem, on_delete=models.CASCADE, parent_link=True, default=0)

    
class GoldGuest(LoyaltySystem):
    loyaltysystem_ptr = models.OneToOneField(LoyaltySystem, on_delete=models.CASCADE, parent_link=True, default=0)

    

class DiamondGuest(LoyaltySystem):
    loyaltysystem_ptr = models.OneToOneField(LoyaltySystem, on_delete=models.CASCADE, parent_link=True, default=0)
