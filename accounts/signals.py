from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver 
from loyaltySystem.models import LoyaltySystem, StandardGuest, SilverGuest, GoldGuest, DiamondGuest
from .models import Guest

@receiver(user_logged_in)
def custom_user_logged_in(sender, request, user, **kwargs):
    # Check if the user is an instance of the Guest model
    if isinstance(user, Guest):
        loyalty_system = LoyaltySystem.objects.get_or_create(user=user)[0]
        loyalty_system.update_membership_tier()

@receiver(post_save, sender=Guest)
def create_loyalty_system(sender, instance, created, **kwargs):
    if created:
        LoyaltySystem.objects.create(user=instance, name=instance.email)