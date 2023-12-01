from hotel.models import Room


def get_room_type(type):
    room = Room.objects.all()[0]
    room_type_name = dict(room.ROOM_TYPES).get(type, None)
    
    return room_type_name