# from django.contrib.auth.signals import user_logged_in
# from django.db.models.signals import post_save
# from django.contrib.auth.models import Group
# from django.dispatch import receiver 
# from loyaltySystem.models import LoyaltySystem, StandardGuest, SilverGuest, GoldGuest, DiamondGuest
# from .models import User

# #after a new user is created and assigned to the guest group, new instance of loyalty is created
# @receiver(post_save, sender=User)
# def create_loyalty_system(sender, instance, created, **kwargs):
#     # Check if the user is created and belongs to the 'guest' group
#     if created and Group.objects.filter(name='guest').exists() and instance.groups.filter(name='guest').exists():
#         LoyaltySystem.objects.create(user=instance, name=instance.username)

#for updating membership tier, checks user logged in is guest
# @receiver(user_logged_in)
# def custom_user_logged_in(sender, request, user, **kwargs):
#     # Check if the user is in the 'guest' group
#     if user.groups.filter(name='guest').exists():
#         # Retrieve the LoyaltySystem instance for the user
#         loyalty_system, created = LoyaltySystem.objects.get_or_create(user=user)

#         # Update the membership tier
#         loyalty_system.update_membership_tier(user)