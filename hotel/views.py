from django.shortcuts import render

from hotel.room_functions.get_room_list import get_room_type_url_list

# Create your views here.
#  seeimg rooms
def room_list_view(request):
    room_list = get_room_type_url_list()
    context = {
        "room_list": room_list,
    }
    return render(request, 'room_list_view.html', context)