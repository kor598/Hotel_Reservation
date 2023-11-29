from bookings.booking_functions.availability import check_availability
from bookings.models import Room

# takes in a type and returns a list of rooms
def get_available_rooms(room_type, check_in_date, check_out_date):
    
    # query set of rooms that matches the type
    room_list = Room.objects.filter(room_type=room_type)
    
    
    # init empty list
    available_rooms = []
        
    # checks if room is available for the selected dates. populates
    for room in room_list:
        if check_availability(room, check_in_date, check_out_date):
            available_rooms.append(room)
    
    # check for length of list
    if len(available_rooms) > 0:
        return available_rooms
    else:
        return None