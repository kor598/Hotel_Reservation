from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

#custom user manager that overrides djangos
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
    #create superuser necessary as overridden djangos usermamager
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password=password, **extra_fields)  
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
#this is used in the guestregister view
    def create_guest(self, email, username, password=None, **extra_fields):
        from loyaltySystem.models import LoyaltySystem
        user = self.create_user(email, username=username, password=password, **extra_fields)
        guests_group, _ = Group.objects.get_or_create(name='Guests')
        user.groups.add(guests_group)
        LoyaltySystem.objects.create(user=user, name=user.username)
        return user
    
    def create_cleaner(self, email, username, password=None, **extra_fields):
        user = self.create_user(email, username=username, password=password, **extra_fields)
        cleaner_group, _ = Group.objects.get_or_create(name='Cleaners')
        user.groups.add(cleaner_group)
        return user
#custom user and assign to usermanager
class User(AbstractUser):
    objects = UserManager()
