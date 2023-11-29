from bookings.models import Booking, Room

def book_room( request, room, check_in, check_out):
    try:
        booking = Booking.objects.create(
            user=request.user,  
            room = room,
            #check_in = data['check_in'],
            #check_out = data['check_out']
            check_in = check_in,
            check_out = check_out,
        )        
        booking.save()
        
        return booking
    except Exception as e:
        print(e)  
        return None

