
import datetime
from bookings.models import Room, Booking

# checks availability of rooms when booking
def check_availability(room, check_in, check_out):
    
    # Check if check_in and check_out are datetime objects. If not, convert them
    if not isinstance(check_in, datetime.datetime) or not isinstance(check_out, datetime.datetime):
        try:
            check_in = datetime.datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            return False 
    
    avail_list = []
    booking_list = Booking.objects.filter(room=room)
    for booking in booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)