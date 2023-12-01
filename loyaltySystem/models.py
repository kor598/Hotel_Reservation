from django.db import models
from datetime import datetime, timedelta
from django.db.models.signals import post_save

from django.dispatch import receiver
from bookings.models import Booking
from accounts.models import User

class LoyaltySystem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Guests'})
    total_points = models.IntegerField(default=0)
    membership_tier = models.CharField(max_length=50, default="Standard")
    
    def calculate_points(self, nights):
        loyalty_points = {
            "Standard": 100,
            "Silver": 110,
            "Gold": 125,
            "Diamond": 150
        }
        self.total_points += nights * loyalty_points.get(self.membership_tier, 0)

    def update_membership_tier(self):
        bookings_list = Booking.objects.filter(user=self.user)
        relevant_bookings_list = bookings_list.filter(check_in_date__gte=datetime.now() - timedelta(days=366))
        total_nights_stayed = sum(Booking.number_of_nights in relevant_bookings_list)

        if total_nights_stayed >= 100:
            self.membership_tier = "Diamond"
        elif total_nights_stayed >= 50:
            self.membership_tier = "Gold"
        elif total_nights_stayed >= 20:
            self.membership_tier = "Silver"

    #def apply_discount(self):
        #discount_percentage = min(self.total_points // 1000 * 10, 50)
        #return discount_percentage 
   
#These subclasses inherit from Loyalty System
#They override the update_membership_tier method to provide specific behaviour for each membership tiers
class StandardGuest(LoyaltySystem):
    def update_membership_tier(self):
        super().update_membership_tier()
        stays_last_366_days = self.stays.filter(date__gte=datetime.now() - timedelta(days=366))
        if stays_last_366_days.count() < 20:
            self.membership_tier = "Standard"

class SilverGuest(LoyaltySystem):
    def update_membership_tier(self):
        super().update_membership_tier()
        stays_last_366_days = self.stays.filter(date__gte=datetime.now() - timedelta(days=366))
        if stays_last_366_days.count() >= 20:
            self.membership_tier = "Silver"
            
class GoldGuest(LoyaltySystem):
    def update_membership_tier(self):
        super().update_membership_tier()
        stays_last_366_days = self.stays.filter(date__gte=datetime.now() - timedelta(days=366))
        if stays_last_366_days.count() >= 50:
            self.membership_tier = "Gold"

class DiamondGuest(LoyaltySystem):
    def update_membership_tier(self):
        super().update_membership_tier()
        stays_last_366_days = self.stays.filter(date__gte=datetime.now() - timedelta(days=366))
        if stays_last_366_days.count() >= 100:
            self.membership_tier = "Diamond"