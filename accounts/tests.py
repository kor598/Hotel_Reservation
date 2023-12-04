from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from hotel.models import Room

class UserModelTest(TestCase):
    def setUp(self):
        self.default_group, _ = Group.objects.get_or_create(name='Default')
        self.supers_group, _ = Group.objects.get_or_create(name='Supers')
        self.admins_group, _ = Group.objects.get_or_create(name='Admin')
        self.guests_group, _ = Group.objects.get_or_create(name='Guests')
        self.cleaners_group, _ = Group.objects.get_or_create(name='Cleaners')

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))
        self.assertTrue(user.groups.filter(name='Default').exists())

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            email='superuser@example.com',
            password='superuserpassword'
        )
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertTrue(superuser.check_password('superuserpassword'))
        self.assertTrue(superuser.groups.filter(name='Supers').exists())

    def test_create_admin(self):
        User = get_user_model()
        admin = User.objects.create_admin(
            email='admin@example.com',
            password='adminpassword'
        )
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertTrue(admin.check_password('adminpassword'))
        self.assertTrue(admin.groups.filter(name='Admin').exists())

    def test_create_guest(self):
        Guest = get_user_model()
        guest = Guest.objects.create_guest(
            email='guest@example.com',
            password='guestpassword',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(guest.email, 'guest@example.com')
        self.assertTrue(guest.check_password('guestpassword'))
        self.assertTrue(guest.groups.filter(name='Guests').exists())

    def test_create_cleaner(self):
        Cleaner = get_user_model()
        room = Room.objects.create()  # You need to create a Room instance for testing
        cleaner = Cleaner.objects.create_cleaner(
            email='cleaner@example.com',
            password='cleanerpassword',
            first_name='Jane',
            last_name='Doe',
            hotel_id=room
        )
        self.assertEqual(cleaner.email, 'cleaner@example.com')
        self.assertTrue(cleaner.check_password('cleanerpassword'))
        self.assertTrue(cleaner.groups.filter(name='Cleaners').exists())
        self.assertEqual(cleaner.hotel_id, room)

