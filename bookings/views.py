from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import AvailabilityForm

from bookings.booking_functions.availability import check_availability
from bookings.booking_functions.get_room_list import get_room_type_url_list
from bookings.booking_functions.get_room_type import get_room_type

from bookings.models import Room, Booking
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.views.generic import DeleteView

# Create your views here.


#  seeimg rooms
def RoomListView(request):
    room_list = get_room_type_url_list()
    context = {
        "room_list": room_list,
    }
    return render(request, 'room_list_view.html', context)

class BookingListView(ListView):
    model = Booking
    template_name = 'booking_list_view.html'
    
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
        room_type_name = get_room_type(type)
        
        form = AvailabilityForm()
        if room_type_name is not None:            
            context = {
                'room_type': room_type_name,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Invalid room type')
        
    def post(self, request, *args, **kwargs):
        room_type = self.kwargs.get('type', None)
        room_list = Room.objects.filter(room_type=room_type)
        form = AvailabilityForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            available_rooms = []
            for room in room_list:
                if check_availability(room, data['check_in'], data['check_out']):
                    available_rooms.append(room)
                
            if len(available_rooms) > 0:        
                room = available_rooms[0]
                
                booking = Booking.objects.create(
                    user=self.request.user,  
                    room = room,
                    check_in = data['check_in'],
                    check_out = data['check_out']
                )        
                booking.save()
                messages.success(self.request, f'Your booking for {room} from {data["check_in"]} to {data["check_out"]} has been confirmed!! Thank you for choosing us.')
                return HttpResponse(booking)
        else:
            return HttpResponse('No rooms available for the selected dates. Please try a different room or date.')

class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('bookings:BookingListView')