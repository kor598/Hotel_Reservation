from django.urls import reverse
from hotel.models import Room

# function that returns list of rooms

def get_room_type_url_list():
    room = Room.objects.first()  # Fetch the first room object
    room_types = dict(room.ROOM_TYPES) if room else {}  # Creating dictionary from room types tuple
    
    room_type_url_list = []
    for room_type, room_name in room_types.items():
        room_url = reverse('bookings:RoomDetailView', kwargs={'type': room_type})
        room_type_url_list.append((room_name, room_url))  # Changed room to room_name
        
    return room_type_url_list