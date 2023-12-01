import logging
from django.db import models

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

class Room(models.Model):
    ROOM_TYPES = (
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('FAMILY', 'Family'),
    )

    room_status = models.CharField(
        max_length=20,
        # Assuming RoomStatus is defined somewhere else
        choices=[
            (status.value, status.name) for status in RoomStatus
        ],
        default=RoomStatus.CLEANED.value,
    )
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    room_beds = models.IntegerField()
    room_capacity = models.IntegerField()
    room_price = models.IntegerField()
    room_description = models.TextField()
    room_image = models.ImageField(upload_to='static/images')
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.room_number}: {self.room_type} with {self.room_beds} beds for {self.room_capacity} people'
    
    def check_in(self):
        self.room_status = RoomStatus.CHECKED_IN.value
        self.save()
        logger = logging.getLogger(__name__)
        logger.info(f"Room {self.room_number} checked in successfully")

    def check_out(self):
        self.room_status = RoomStatus.CHECKED_OUT.value
        self.save()
        logger = logging.getLogger(__name__)
        logger.info(f"Room {self.room_number} checked out successfully")

    def clean_room(self):
        self.room_status = RoomStatus.CLEANED.value
        self.save()
        logger = logging.getLogger(__name__)
        logger.info(f"Room {self.room_number} is clean!")
        
