from django.core.management.base import BaseCommand
from hotel.models import Hotel

class Command(BaseCommand):
    help = 'Deletes hotels based on criteria'

    def add_arguments(self, parser):
        parser.add_argument('hotel_name', nargs='+', type=str, help='Name of the hotel to delete')

    def handle(self, *args, **kwargs):
        hotel_names = kwargs['hotel_name']
        for name in hotel_names:
            try:
                hotel = Hotel.objects.get(name=name)
                # Delete associated rooms before deleting the hotel
                rooms = hotel.rooms.all()
                for room in rooms:
                    room.delete()
                hotel.delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted {name} and its rooms'))
            except Hotel.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Hotel with name {name} does not exist'))