from django.db import models
from datetime import datetime, timedelta

class LoyaltySystemManager(models.Manager):
    pass

class LoyaltySystem(models.Model):
    from accounts.models import Guest
    user = models.OneToOneField(Guest, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_points = models.IntegerField(default=0)
    membership_tier = models.CharField(max_length=50, default="Standard")
    last_checkin_date = models.DateTimeField(auto_now_add=True)
    
    objects = LoyaltySystemManager()

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
