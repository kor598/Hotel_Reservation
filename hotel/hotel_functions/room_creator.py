from hotel.models import Hotel
from hotel.room_factory import RoomFactory

def create_rooms_for_standard_hotel(hotel_name, num_rooms):
    # calculate the distribution of rooms among different types
    num_single = num_rooms // 3  # Dividing among single, double, and family rooms equally, or as equally as possible
    num_double = num_rooms // 3
    num_family = num_rooms - (num_single + num_double)

    created_rooms = []

    # creates hotel
    existing_hotel = Hotel.objects.filter(name=hotel_name).first()

    if not existing_hotel:
        new_hotel = Hotel.objects.create(
            name=hotel_name,
            address=f'{hotel_name} Address',  
            number_of_rooms=num_rooms
        )

        # Create rooms 
        for i in range(num_single):
            room = RoomFactory.create_single_room(
                room_number=f'1{i + 1}', # room numbers for single all start with 1
                room_beds=1,
                room_capacity=1,
                room_price=100,
                room_description=f'Description of Single Room 1{i + 1}',
                room_image='hotel/static/images/single_room.jpg',
                hotel=new_hotel  # Assign the hotel to the room
            )
            created_rooms.append(room)

        for i in range(num_double):
            room = RoomFactory.create_double_room(
                room_number=f'2{i + 1}',
                room_beds=2,
                room_capacity=2,
                room_price=150,
                room_description=f'Description of Double Room 2{i + 1}',
                room_image='hotel/static/images/double_room.jpg',
                hotel=new_hotel  # Assign the hotel to the room
            )
            created_rooms.append(room)

        for i in range(num_family):
            room = RoomFactory.create_family_room(
                room_number=f'3{i + 1}',
                room_beds=3,
                room_capacity=4,
                room_price=200,
                room_description=f'Description of Family Room 3{i + 1}',
                room_image='hotel/static/images/family_room.jpg',
                hotel=new_hotel  # Assign the hotel to the room
            )
            created_rooms.append(room)

        return created_rooms # Success, returning the created rooms

    return None