from django.db import models
from accounts.models import User
from .room_status import RoomStatus
# Create your models here.
class Room(models.Model):
    ROOM_TYPES = (
        # key, value
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('FAMILY', 'Family'),
    )

    status = models.CharField(
        max_length=20,
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

    def __str__(self):
        return f'{self.room_number}: {self.room_type} with {self.room_beds} beds for {self.room_capacity} people'
    
    def check_in(self):
        self.status = RoomStatus.CHECKED_IN.value
        self.save()

    def check_out(self):
        self.status = RoomStatus.CHECKED_OUT.value
        self.save()

    def clean_room(self):
        self.status = RoomStatus.CLEANED.value
        self.save()
    
class Booking(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)  # Ensure it's referencing the correct User model
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()

    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in_date} to {self.check_out_date}'
    
    
    