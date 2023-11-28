from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class LoyaltySystem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Add this line to link with the User model
    name = models.CharField(max_length=255)
    total_points = models.IntegerField(default=0)
    membership_tier = models.CharField(max_length=50, default="Standard")
    last_checkin_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def calculate_points(self, nights):
        loyalty_points = {
            "Standard": 100,
            "Silver": 110,
            "Gold": 125,
            "Diamond": 150
        }
        self.total_points += nights * loyalty_points.get(self.membership_tier, 0)

    def update_membership_tier(self):
        stays_last_366_days = self.stays.filter(date__gte=datetime.now() - timedelta(days=366))
        nights_stayed = sum(stay.nights for stay in stays_last_366_days)

        if nights_stayed >= 100:
            self.membership_tier = "Diamond"
        elif nights_stayed >= 50:
            self.membership_tier = "Gold"
        elif nights_stayed >= 20:
            self.membership_tier = "Silver"

    def apply_discount(self):
        discount_percentage = min(self.total_points // 1000 * 10, 50)
        return discount_percentage


class Stay(models.Model):
    guest = models.ForeignKey(LoyaltySystem, on_delete=models.CASCADE, related_name='stays')
    date = models.DateTimeField(auto_now_add=True)
    nights = models.IntegerField(default=1)
    
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
