from django.contrib.auth.signals import user_logged_in, post_save
from django.dispatch import receiver 
from loyaltySystem.models import LoyaltySystem, StandardGuest, SilverGuest, GoldGuest, DiamondGuest
from .models import User

@receiver(user_logged_in)
def custom_user_logged_in(sender, request, user, **kwargs):
    # Check if the user is in the 'guest' group
    if user.groups.filter(name='guest').exists():
        LoyaltySystem().update_membership_tier(user)

@receiver(post_save, sender=User)
def create_loyalty_system(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name='Guests').exists():
        LoyaltySystem.objects.create(user=instance, name=instance.username)