from django.urls import reverse
from hotel.models import Room

# function that returns list of rooms


def get_room_type_url_list(rooms):
    room_type_url_list = []
    added_room_types = set()  # Keep track of added room types
    
    for room in rooms:
        if room.room_type not in added_room_types:
            room_url = reverse('bookings:RoomDetailView', kwargs={'type': room.room_type})
            room_type_url_list.append((room.room_type, room_url))
            added_room_types.add(room.room_type)  # Add the room type to the set
    
    return room_type_url_list