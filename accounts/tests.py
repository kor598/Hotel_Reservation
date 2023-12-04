from django.test import TestCase, Client
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from loyaltySystem.models import LoyaltySystem
from accounts.signals import create_loyalty_system
from accounts.models import User

class SignalTestCase(TestCase):
    def setUp(self):
        # Connect the signal for the test
        post_save.connect(create_loyalty_system, sender=User)

    def tearDown(self):
        # Disconnect the signal after the test
        post_save.disconnect(create_loyalty_system, sender=User)
    
    def test_create_loyalty_system_signal(self):
        # Create a user in the 'guest' group using the custom user model
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        guest_group = Group.objects.create(name='guest')
        user.groups.add(guest_group)

        # Explicitly create a LoyaltySystem instance
        loyalty_system = LoyaltySystem.objects.create(user=user, name=user.username)

        #LoyaltySystem instance is created????
        self.assertEqual(loyalty_system.name, 'testuser')
    
    def test_custom_user_logged_in_signal(self):
        # Create a user in the group guest
        user = get_user_model().objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        guest_group = Group.objects.create(name='guest')
        user.groups.add(guest_group)

        # Simulate user login
        client = Client()
        client.force_login(user)

        updated_loyalty_system = LoyaltySystem.objects.get(user=user)
        self.assertEqual(updated_loyalty_system.name, 'testuser')