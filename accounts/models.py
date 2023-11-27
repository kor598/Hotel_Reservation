from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        GUEST = "GUEST", "Guest"
        STAFF = "STAFF", "Staff"
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:  # Checking if it's a new record
            self.role = User.Role.GUEST  # Set default role as Guest
        super().save(*args, **kwargs)


class GuestManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.GUEST)


class Guest(User):

    base_role = User.Role.GUEST

    Guest = GuestManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for guests"


@receiver(post_save, sender=Guest)
def create_guest_profile(sender, instance, created, **kwargs):
    if created and instance.role == "GUEST":
        GuestProfile.objects.create(user=instance)

#add additional fields here
class GuestProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    guest_id = models.IntegerField(null=True, blank=True)
    # firstname = models.CharField(max_length=255)
    # lastname = models.CharField(max_length=255)

class StaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STAFF)


class Staff(User):

    base_role = User.Role.STAFF

    staff = StaffManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for staff"

#add additional fields here
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=Staff)
def create_staff_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STAFF":
        StaffProfile.objects.create(user=instance)