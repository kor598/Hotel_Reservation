from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import ListView, FormView, View
from django.urls import reverse
from .forms import AvailabilityForm
from bookings.availability import check_availability
from bookings.models import Room, Booking
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User

# Create your views here.
def CheckInView(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.check_in()
    return render(request, 'check_in_success.html', {'room': room})

def CheckOutView(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.check_out()
    return render(request, 'check_out_success.html', {'room': room})

# temp view to see rooms
def RoomListView(request):
    room = Room.objects.all()[0]
    room_types = dict(room.ROOM_TYPES)
    print('types = ', room_types)
    
    room_values = room_types.values()
    print('values = ', room_values)
    room_list = []
    
    for room_type in room_types:
        room = room_types.get(room_type)
        room_url = reverse('bookings:RoomDetailView', kwargs={
                            'type': room_type})
        room_list.append((room, room_url))
    
    context = {
        "room_list": room_list,
    }
    return render(request, 'room_list_view.html', context)

class BookingList(ListView):
    model = Booking
    template_name = 'booking_list.html'
    context_object_name = 'booking_list'
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list
    
    
#     actual room view
class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        # if people type the wrong thing
        type = self.kwargs.get('type', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(room_type= type)
        # takes first room in list
        
        if len(room_list) > 0:
            room = room_list[0]
            room_type_name = dict(room.ROOM_TYPES).get(type, None)
            context = {
                'room_type': room_type_name,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Room no existo')
        
        
        
    def post(self, request, *args, **kwargs):
        room_type = self.kwargs.get('type', None)
        room_list = Room.objects.filter(room_type=room_type)
        data = request.POST
        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in_date'], data['check_out_date']):
                available_rooms.append(room)
                
        if len(available_rooms) > 0:        
            room = available_rooms[0]
                
            booking = Booking.objects.create(
                user=self.request.user,  
                room = room,
                check_in_date = data['check_in_date'],
                check_out_date = data['check_out_date']
            )        
            booking.save()
            messages.success(self.request, f'Your booking for {room} from {data["check_in_date"]} to {data["check_out_date"]} has been confirmed!! Thank you for choosing us.')
            return HttpResponse(booking)
        else:
            return HttpResponse('No rooms available for the selected dates. Please try a different room or date.')
    
class BookingForm(LoginRequiredMixin, FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(room_type=data['room_type'])
        available_rooms = [room for room in room_list if check_availability(room, data['check_in_date'], data['check_out_date'])]

        if available_rooms:
            room = available_rooms[0]

            booking = Booking.objects.create(
                user=self.request.user,  
                room=room,
                check_in=data['check_in_date'],
                check_out=data['check_out_date']
            )
            booking.save()

            messages.success(
                self.request,
                f'Your booking for {room} from {data["check_in_date"]} to {data["check_out_date"]} has been confirmed!! Thank you for choosing us.'
            )
            return HttpResponse('Booking created {guest_user}!')
        else:
            return HttpResponse('No rooms available for the selected dates. Please try a different room or date.')
        
