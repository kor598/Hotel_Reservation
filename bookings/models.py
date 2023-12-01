from django.db import models
from django.urls import reverse_lazy
from accounts.models import User
from hotel.models import Room

# Create your models here.
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ensure it's referencing the correct User model
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in_date} to {self.check_out_date}'
    
    def get_room_type(self):
        room_types = dict(self.room.ROOM_TYPES)
        room_type = room_types.get(self.room.room_type)
        return room_type
    
    def get_cancel_booking_url(self):
        return reverse_lazy('bookings:CancelBookingView', args = [self.pk ])
    