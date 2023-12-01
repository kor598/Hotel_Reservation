from django.core.management.base import BaseCommand
from hotel.models import Room

class Command(BaseCommand):
    help = 'Deletes all rooms'

    def handle(self, *args, **options):
        Room.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All rooms deleted'))