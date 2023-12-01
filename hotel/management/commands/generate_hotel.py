from django.core.management.base import BaseCommand
from hotel.views import create_rooms_for_standard_hotel

class Command(BaseCommand):
    help = 'Generates a hotel with rooms'

    def add_arguments(self, parser):
        parser.add_argument('hotel_name', type=str, help='Name of the hotel')
        parser.add_argument('num_rooms', type=int, help='Number of rooms to generate')

    def handle(self, *args, **options):
        hotel_name = options['hotel_name']
        num_rooms = options['num_rooms']

        created_rooms = create_rooms_for_standard_hotel(hotel_name, num_rooms)

        if created_rooms:
            self.stdout.write(self.style.SUCCESS(f'Created {len(created_rooms)} rooms for {hotel_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Failed to create rooms for {hotel_name}'))