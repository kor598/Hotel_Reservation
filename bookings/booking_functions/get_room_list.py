from django.urls import reverse
from bookings.models import Room

# function that returns list of rooms
def get_room_type_url_list():
    room = Room.objects.all()[0] # gets a random room object
    room_types = dict(room.ROOM_TYPES) # creates a dictionary from the room types tuple
    
    # room_values = room_types.values()
    # print('values = ', room_values)
    room_type_url_list = []
    for room_type in room_types: # populates room type url list with tuples of room type and url
        room = room_types.get(room_type)
        room_url = reverse('bookings:RoomDetailView', kwargs={
                            'type': room_type})
        room_type_url_list.append((room, room_url))
        
    return room_type_url_list