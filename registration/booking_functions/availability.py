import datetime
from registration.models import Room, Booking

# checks availability of rooms when booking
def check_availability(room, check_in, check_out):
    avail_list = []
    booking_list = Booking.objects.filter(room=room)
    for booking in booking_list:
        if booking.check_in > check_out or booking.check_out < check_in:
            avail_list.append(True)
        else:
            avail_list.append(False)
    return all(avail_list)
            