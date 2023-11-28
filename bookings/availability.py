
import datetime
from bookings.models import Room, Booking

# checks availability of rooms when booking
def check_availability(room, check_in_date, check_out_date):
    
    # Check if check_in and check_out are datetime objects. If not, convert them
    if not isinstance(check_in_date, datetime.datetime) or not isinstance(check_out_date, datetime.datetime):
        try:
            check_in_date = datetime.datetime.strptime(check_in_date, "%Y-%m-%d").date()
            check_out_date = datetime.datetime.strptime(check_out_date, "%Y-%m-%d").date()
        except ValueError:
            return False 
    
    avail_list = []
    booking_list = Booking.objects.filter(room=room)
    for booking in booking_list:
        if booking.check_in_date > check_out_date or booking.check_out_date < check_in_date:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)