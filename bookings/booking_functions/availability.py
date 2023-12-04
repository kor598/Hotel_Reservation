
import datetime
from datetime import date
from bookings.models import Room, Booking

# checks availability of room. 
def check_availability(room, check_in_date, check_out_date):
    # filters bookings for the room, and checks check_in overlaps
    overlapping_bookings = Booking.objects.filter(
        room=room,
        check_in_date__lt=check_out_date,
        check_out_date__gt=check_in_date
    )
    return not overlapping_bookings.exists()

'''
def check_availability(room, check_in, check_out):
    avail_list = []
    booking_list = Booking.objects.filter(room=room)
    for booking in booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)
    '''