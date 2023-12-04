from datetime import date
import logging
from django.db import models
from loyaltySystem.models import LoyaltySystem
from hotel.room_status import RoomStatus

# creates a hotel
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    number_of_rooms = models.PositiveIntegerField()

    def __str__(self):
        return self.name

'''
To stop circular dependency, we can use the string 'Room' instead of the Room class
'''
# junction table
class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room.room_number}"

# creates a room
class Room(models.Model):
    ROOM_TYPES = (
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('FAMILY', 'Family'),
    )

    room_number = models.IntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    room_beds = models.IntegerField()
    room_capacity = models.IntegerField()
    room_price = models.IntegerField()
    room_description = models.TextField()
    room_image = models.ImageField(upload_to='static/images')
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE, default=1)

    room_status = models.CharField(
        max_length=20,
        choices=[
            (status.value, status.name) for status in RoomStatus
        ],
        default=RoomStatus.CLEANED.value,
    )
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.room_number}: {self.room_type} with {self.room_beds} beds for {self.room_capacity} people'

    def set_status(self, new_status):
        self.room_status = new_status
        self.save()

    def handle_state(self, state):
        return state.handle(self)

class RoomState:
    def handle(self, room):
        pass

class CheckedInState(RoomState):
    def handle(self, room):
        today = date.today()
        # Get all bookings for this room
        room_bookings = room.booking_set.filter(check_in_date__date=today)

        relevant_booking = room_bookings.first()

        if relevant_booking:
            relevant_booking.calculate_points_earned()
            user = relevant_booking.user
            loyalty_system = LoyaltySystem.objects.get(user=user)
            loyalty_system.total_points += relevant_booking.points_earned
            loyalty_system.update_membership_tier()
            loyalty_system.save()

            room.set_status(RoomStatus.CHECKED_IN.value)

            logger = logging.getLogger(__name__)
            logger.info(f"Room {room.room_number} checked in successfully")

            return relevant_booking.points_earned
        else:
            logger = logging.getLogger(__name__)
            logger.error(f"No booking found for today for Room {room.room_number}")
            return None

class CheckedOutState(RoomState):
    def handle(self, room):
        room.set_status(RoomStatus.CHECKED_OUT.value)
        logger = logging.getLogger(__name__)
        logger.info(f"Room {room.room_number} checked out successfully")

class CleanedState(RoomState):
    def handle(self, room):
        room.set_status(RoomStatus.CLEANED.value)
        logger = logging.getLogger(__name__)
        logger.info(f"Room {room.room_number} is clean!")

    def check_out(self, room):
        room.set_status(RoomStatus.CHECKED_OUT.value)
        logger = logging.getLogger(__name__)
        logger.info(f"Room {room.room_number} checked out successfully")