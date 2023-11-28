from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

####Managers##########################################

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class GuestManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.GUEST)
    
class StaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STAFF)

###################Defining abstract user and roles
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

    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email_parts = email.split('@')
        email_parts[-1] = email_parts[-1].lower()
        return '@'.join(email_parts)
    
    objects = UserManager() 

####User role classes#################
class Guest(User):

    base_role = User.Role.GUEST

    Guest = GuestManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for guests"


@receiver(post_save, sender=Guest)
def create_guest_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.GUEST:
        GuestProfile.objects.create(user=instance)

#add additional fields here
class GuestProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    guest_id = models.IntegerField(null=True, blank=True)
    # firstname = models.CharField(max_length=255)
    # lastname = models.CharField(max_length=255)

class Staff(User):

    base_role = User.Role.STAFF

    staff = StaffManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for staff"

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=Staff)
def create_staff_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.STAFF:
        StaffProfile.objects.create(user=instance)