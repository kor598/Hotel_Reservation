from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from hotel.models import Room
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        default_group, _ = Group.objects.get_or_create(name='Default')
        user.save(using=self._db)
        user.groups.add(default_group)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password=password, **extra_fields)  
        supers_group, _ = Group.objects.get_or_create(name='Supers')
        user.groups.add(supers_group)
        return user
    
    def create_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        user = self.create_user(email, password=password, **extra_fields)
        admins_group, _ = Group.objects.get_or_create(name='Admin')
        user.groups.add(admins_group)
        return user

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Guest(User):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    def create_guest(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        guests_group, _ = Group.objects.get_or_create(name='Guests')
        user.groups.add(guests_group)
        return user

class Cleaner(User):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hotel_id = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='cleaners')
    def create_cleaner(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        cleaner_group, _ = Group.objects.get_or_create(name='Cleaners')
        user.groups.add(cleaner_group)
        return user
