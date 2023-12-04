from django.db import models
from datetime import datetime, timedelta, timezone
from accounts.models import User
from django.utils import timezone

class LoyaltySystemManager(models.Manager):
    pass

class LoyaltySystem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_points = models.IntegerField(default=0)
    membership_tier = models.CharField(max_length=50, default="Standard")
    last_checkin_date = models.DateTimeField(auto_now_add=True)
    
    objects = LoyaltySystemManager()

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

        if total_nights >= 100:
            self.membership_tier = "Diamond"
        elif total_nights >= 50:
            self.membership_tier = "Gold"
        elif total_nights >= 20:
            self.membership_tier = "Silver"
            
        self.save()
        
class StandardGuest(LoyaltySystem):
    loyaltysystem_ptr = models.OneToOneField(LoyaltySystem, on_delete=models.CASCADE, parent_link=True, default=0)

    def update_membership_tier(self):
        super().update_membership_tier()
        stays_last_366_days = self.stays.filter(date__gte=datetime.now() - timedelta(days=366))
        if stays_last_366_days.count() < 20:
            self.membership_tier = "Standard"

class SilverGuest(LoyaltySystem):
    loyaltysystem_ptr = models.OneToOneField(LoyaltySystem, on_delete=models.CASCADE, parent_link=True, default=0)

    def update_membership_tier(self):
        super().update_membership_tier()
        stays_last_366_days = self.stays.filter(date__gte=datetime.now() - timedelta(days=366))
        if stays_last_366_days.count() >= 20:
            self.membership_tier = "Silver"
            
class GoldGuest(LoyaltySystem):
    loyaltysystem_ptr = models.OneToOneField(LoyaltySystem, on_delete=models.CASCADE, parent_link=True, default=0)

    def update_membership_tier(self):
        super().update_membership_tier()
        stays_last_366_days = self.stays.filter(date__gte=datetime.now() - timedelta(days=366))
        if stays_last_366_days.count() >= 50:
            self.membership_tier = "Gold"

class DiamondGuest(LoyaltySystem):
    loyaltysystem_ptr = models.OneToOneField(LoyaltySystem, on_delete=models.CASCADE, parent_link=True, default=0)
    def update_membership_tier(self):
        super().update_membership_tier()
        stays_last_366_days = self.stays.filter(date__gte=datetime.now() - timedelta(days=366))
        if stays_last_366_days.count() >= 100:
            self.membership_tier = "Diamond"