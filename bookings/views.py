from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import ListView, FormView, View
from .forms import AvailabilityForm
from bookings.availability import check_availability
from bookings.models import Room, Booking

# Create your views here.


# temp view to see rooms
class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html' 
    context_object_name = 'room_list'

class BookingList(ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'booking_list'
    
#     actual room view
class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        # if people type the wrong thing
        room_type = self.kwargs.get('type', None)
        # room_list = Room.objects.filter(room_type= room_type)
        # takes first room in list
        # room = room_type[0]
        context = {
            'room_type': room_type
        }
        return render(request, 'room_detail_view.html', context)
        
        
        
    def post(self, request, *args, **kwargs):
        room_type = self.kwargs.get('type', None)
        room_list = Room.objects.filter(room_type=room_type)
        data = request.POST
        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
                
        if len(available_rooms) > 0:        
            room = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )        
            booking.save()
            messages.success(self.request, f'Your booking for {room} from {data["check_in"]} to {data["check_out"]} has been confirmed!! Thank you for choosing us.')
            return HttpResponse(booking)
        else:
            return HttpResponse('No rooms available for the selected dates. Please try a different room or date.')
    
class BookingForm(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'
    
    def form_valid(self,form):
        data = form.cleaned_data
        room_list = Room.objects.filter(room_type=data['room_type'])
        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
                
        if len(available_rooms) > 0:        
            room = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )        
            booking.save()
            messages.success(self.request, f'Your booking for {room} from {data["check_in"]} to {data["check_out"]} has been confirmed!! Thank you for choosing us.')
            return HttpResponse(booking)
        else:
            return HttpResponse('No rooms available for the selected dates. Please try a different room or date.')