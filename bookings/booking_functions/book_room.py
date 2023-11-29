from bookings.models import Booking, Room

def book_room(request, room, check_in_date, check_out_date):
    try:
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            check_in_date=check_in_date,  # Updated field name
            check_out_date=check_out_date,  # Updated field name
        )
        return booking
    except Exception as e:
        print(e)
        return None

