from .models import Room

class RoomFactory:
    @staticmethod
    def create_room(room_number, room_type, room_beds, room_capacity, room_price, room_description, room_image, hotel=None):
        room = Room.objects.create(
            room_number=room_number,
            room_type=room_type,
            room_beds=room_beds,
            room_capacity=room_capacity,
            room_price=room_price,
            room_description=room_description,
            room_image=room_image,
            room_status='cleaned',
            hotel=hotel  # Associate the room with the hotel
        )
        return room

    @classmethod
    def create_single_room(cls, room_number, room_beds, room_capacity, room_price, room_description, room_image, hotel=None):
        return cls.create_room(room_number, 'SINGLE', room_beds, room_capacity, room_price, room_description, room_image, hotel)

    @classmethod
    def create_double_room(cls, room_number, room_beds, room_capacity, room_price, room_description, room_image, hotel=None):
        return cls.create_room(room_number, 'DOUBLE', room_beds, room_capacity, room_price, room_description, room_image, hotel)

    @classmethod
    def create_family_room(cls, room_number, room_beds, room_capacity, room_price, room_description, room_image, hotel=None):
        return cls.create_room(room_number, 'FAMILY', room_beds, room_capacity, room_price, room_description, room_image, hotel)