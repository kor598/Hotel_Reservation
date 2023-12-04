from hotel.models import Room, Hotel

# creatinf rooms for a hotel
def create_rooms_for_hotel(hotel, room_data_list):
    created_rooms = []
    for room_data in room_data_list:
        room = Room.objects.create(**room_data)
        hotel.rooms.add(room)
        created_rooms.append(room)
    return created_rooms