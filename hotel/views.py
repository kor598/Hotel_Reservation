from django.shortcuts import get_object_or_404, render

from hotel.hotel_functions.room_creator import create_rooms_for_standard_hotel
from .models import Hotel, Room

from hotel.room_functions.get_room_list import get_room_type_url_list
from hotel.hotel_functions.create_rooms import create_rooms_for_hotel

# Create your views here.

# Display the list of hotels for selection
def choose_hotel_view(request):
    hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, 'choose_hotel.html', context)

#  seeimg rooms
def room_list_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)  # Filter rooms related to the selected hotel
    room_list = get_room_type_url_list(rooms)
    context = {'hotel': hotel, 'room_list': room_list} 
    return render(request, 'room_list_view.html', context)


def generate_hotel_with_rooms(hotel_name, num_rooms):
    hotel_exists = Hotel.objects.filter(name=hotel_name).exists()

    if hotel_exists:
        existing_hotel = Hotel.objects.get(name=hotel_name)
        return False, existing_hotel  
    else:
        # Create a new hotel with the provided name and number of rooms
        new_hotel = Hotel.objects.create(name=hotel_name, number_of_rooms=num_rooms)

        # Generate rooms for the hotel
        created_rooms = create_rooms_for_hotel(new_hotel, num_rooms)

        if created_rooms:
            return True, created_rooms  
        else:
            return False, new_hotel  