from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        default_group, _ = Group.objects.get_or_create(name='Default')
        user.save(using=self._db)
        user.groups.add(default_group)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password=password, **extra_fields)  # Specify password parameter
        supers_group, _ = Group.objects.get_or_create(name='Supers')
        user.groups.add(supers_group)
        return user
    
    def create_admin(self, email,username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        user = self.create_user(email, username=username, password=password, **extra_fields)
        admins_group, _ = Group.objects.get_or_create(name='Admin')
        user.groups.add(admins_group)
        return user

    def create_guest(self, email, username, password=None, **extra_fields):
        # Create a guest user and assign them to the 'Guests' group
        user = self.create_user(email, username=username, password=password, **extra_fields)
        guests_group, _ = Group.objects.get_or_create(name='Guests')
        user.groups.add(guests_group)
        return user
    
    def create_cleaner(self, email, username, password=None, **extra_fields):
        user = self.create_user(email, username=username, password=password, **extra_fields)
        cleaner_group, _ = Group.objects.get_or_create(name='Cleaners')
        user.groups.add(cleaner_group)
        return user

class User(AbstractUser):
    objects = UserManager()
    
from loyaltySystem.models import LoyaltySystem, StandardGuest, SilverGuest, GoldGuest, DiamondGuest
@receiver(post_save, sender=User)
def create_loyalty_system(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name='Guests').exists():
        LoyaltySystem.objects.create(user=instance, name=instance.username)
