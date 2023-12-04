from datetime import date
import logging
from django.db import models
from loyaltySystem.models import LoyaltySystem
from hotel.room_status import RoomStatus

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    number_of_rooms = models.PositiveIntegerField()

    def __str__(self):
        return self.name

'''
To stop circular dependency, we can use the string 'Room' instead of the Room class
'''
class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room.room_number}"

# State interface
class RoomState:
    def handle(self, room):
        pass

# Concrete State classes
class CheckedInState(RoomState):
    def handle(self, room):
        today = date.today()
        relevant_booking = room.get_relevant_booking(today)

        if relevant_booking:
            relevant_booking.calculate_points_earned()

            user = relevant_booking.user
            loyalty_system = LoyaltySystem.objects.get(user=user)

            loyalty_system.total_points += relevant_booking.points_earned
            loyalty_system.update_membership_tier()
            loyalty_system.save()

            room.room_status = RoomStatus.CHECKED_IN.value
            room.save()

            logger = logging.getLogger(__name__)
            logger.info(f"Room {room.room_number} checked in successfully")

            return relevant_booking.points_earned
        else:
            logger = logging.getLogger(__name__)
            logger.error(f"No booking found for today for Room {room.room_number}")
            return None

class CheckedOutState(RoomState):
    def handle(self, room):
        room.room_status = RoomStatus.CHECKED_OUT.value
        room.save()
        logger = logging.getLogger(__name__)
        logger.info(f"Room {room.room_number} checked out successfully")

class CleanedState(RoomState):
    def handle(self, room):
        room.room_status = RoomStatus.CLEANED.value
        room.save()
        logger = logging.getLogger(__name__)
        logger.info(f"Room {room.room_number} is clean!")

# Context
class Room:
    def __init__(self, room_number):
        self.room_number = room_number
        self.room_status = RoomStatus.CLEANED.value  # Initial state

    def get_relevant_booking(self, today):
        from bookings.models import Booking
        room_bookings = Booking.objects.filter(room_id=self.id)
        relevant_booking = None

        for booking in room_bookings:
            if booking.check_in_date.date() == today:
                relevant_booking = booking
                break  # Found the relevant booking, exit the loop

        return relevant_booking

    def set_state(self, state):
        self._state = state

    def check_in(self):
        self._state.handle(self)

    def check_out(self):
        self._state.handle(self)

    def clean_room(self):
        self._state.handle(self)

    def save(self, *args, **kwargs):
        # Your custom save logic goes here
        super().save(*args, **kwargs)

# room = Room(room_number=101)
# room.set_state(CleanedState())

# room.check_in()
# room.check_out()
# room.clean_room()


# class Room(models.Model):
#     ROOM_TYPES = (
#         ('SINGLE', 'Single'),
#         ('DOUBLE', 'Double'),
#         ('FAMILY', 'Family'),
#     )

#     room_status = models.CharField(
#         max_length=20,
#         # Assuming RoomStatus is defined somewhere else
#         choices=[
#             (status.value, status.name) for status in RoomStatus
#         ],
#         default=RoomStatus.CLEANED.value,
#     )
#     room_number = models.IntegerField()
#     room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
#     room_beds = models.IntegerField()
#     room_capacity = models.IntegerField()
#     room_price = models.IntegerField()
#     room_description = models.TextField()
#     room_image = models.ImageField(upload_to='static/images')
#     hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return f'{self.room_number}: {self.room_type} with {self.room_beds} beds for {self.room_capacity} people'
    
#     def check_in(self):
#         from bookings.models import Booking  # Import here to break the circular dependency

#         today = date.today()

#         # Get all bookings for this room
#         room_bookings = Booking.objects.filter(room_id=self.id)

#         # Filter bookings that have the check-in date as today
#         relevant_booking = None
#         for booking in room_bookings:
#             if booking.check_in_date.date() == today:
#                 relevant_booking = booking
#                 break  # Found the relevant booking, exit the loop

#         if relevant_booking:
#             relevant_booking.calculate_points_earned()

#             user = relevant_booking.user
#             loyalty_system = LoyaltySystem.objects.get(user=user)

#             loyalty_system.total_points += relevant_booking.points_earned
#             loyalty_system.update_membership_tier()
#             loyalty_system.save()

#             self.room_status = RoomStatus.CHECKED_IN.value
#             self.save()

#             logger = logging.getLogger(__name__)
#             logger.info(f"Room {self.room_number} checked in successfully")

#             return relevant_booking.points_earned
#         else:
#             logger = logging.getLogger(__name__)
#             logger.error(f"No booking found for today for Room {self.room_number}")
#             return None  

#     def check_out(self):
#         self.room_status = RoomStatus.CHECKED_OUT.value
#         self.save()
#         logger = logging.getLogger(__name__)
#         logger.info(f"Room {self.room_number} checked out successfully")

#     def clean_room(self):
#         self.room_status = RoomStatus.CLEANED.value
#         self.save()
#         logger = logging.getLogger(__name__)
#         logger.info(f"Room {self.room_number} is clean!")
        

# # State interface
# class RoomState:
#     def handle(self, room):
#         pass

# # Concrete State classes
# class CheckedInState(RoomState):
#     def handle(self, room):
#         room.room_status = RoomStatus.CHECKED_IN.value
#         room.save()
#         logger = logging.getLogger(__name__)
#         logger.info(f"Room {room.room_number} checked in successfully")

# class CheckedOutState(RoomState):
#     def handle(self, room):
#         room.room_status = RoomStatus.CHECKED_OUT.value
#         room.save()
#         logger = logging.getLogger(__name__)
#         logger.info(f"Room {room.room_number} checked out successfully")

# class CleanedState(RoomState):
#     def handle(self, room):
#         room.room_status = RoomStatus.CLEANED.value
#         room.save()
#         logger = logging.getLogger(__name__)
#         logger.info(f"Room {room.room_number} is clean!")


#     def set_state(self, state):
#         self._state = state

#     def check_in(self):
#         self._state.handle(self)

#     def check_out(self):
#         self._state.handle(self)

#     def clean_room(self):
#         self._state.handle(self)

# # Example usage
# room = Room(room_number=101)
# room.set_state(CleanedState())

# room.check_in()
# room.check_out()
# room.clean_room()
