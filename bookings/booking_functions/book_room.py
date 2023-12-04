from bookings.models import Booking
from hotel.models import Room

# books a room for a user
def book_room(request, room, check_in_date, check_out_date):
    # creates a booking object
    try:
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            check_in_date=check_in_date,  
            check_out_date=check_out_date,  
        )
        return booking
    except Exception as e:
        print(e)
        return None

