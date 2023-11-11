from django.db import models
from accounts.models import User

# Create your models here.

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

    def __str__(self):
        return f'{self.room_number}: {self.room_type} with {self.room_beds} beds for {self.room_capacity} people'
    
    
class Booking(models.Model):
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    
    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in} to {self.check_out}'
    
    
    