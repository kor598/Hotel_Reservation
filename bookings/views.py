from datetime import datetime, time
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import AvailabilityForm

from bookings.booking_functions.availability import check_availability
from bookings.booking_functions.get_available_rooms import get_available_rooms
from bookings.booking_functions.book_room import book_room

from hotel.room_functions.get_room_type import get_room_type

from bookings.models import Booking
from hotel.models import Room

from django.views.generic import DeleteView

# Create your views here.
def CheckInView(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.check_in()
    return render(request, 'check_in_success.html', {'room': room})

def CheckOutView(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.check_out()
    return render(request, 'check_out_success.html', {'room': room})



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
        
        # get room type from kwargs
        type = self.kwargs.get('type', None)
        
        # get the room type name from the type
        room_type_name = get_room_type(type)
        
        # init empty form
        form = AvailabilityForm()
        
        # if room type is valid
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
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            # Convert string dates to datetime objects
            check_in_time = data['check_in_date']
            check_out_time = data['check_out_date']

            # Set the time to 4:00 PM for both check-in and check-out
            check_in_time = check_in_time.replace(hour=16, minute=0, second=0)
            check_out_time = check_out_time.replace(hour=16, minute=0, second=0)

            # Add some debugging print statements
            print(check_in_time, check_out_time)
            
            
            available_rooms = get_available_rooms(room_type, check_in_time, check_out_time)
            
            if available_rooms is not None:
                booking = book_room(request, available_rooms[0], check_in_time, check_out_time)

                # Format datetime objects to strings for message display
                formatted_check_in = check_in_time.strftime("%Y-%m-%d %H:%M:%S")
                formatted_check_out = check_out_time.strftime("%Y-%m-%d %H:%M:%S")

                messages.success(
                    self.request,
                    f'Your booking for a {room_type} room from {formatted_check_in} to {formatted_check_out} has been confirmed!! Thank you for choosing us.'
                )
                return HttpResponse(booking)
            else:
                return HttpResponse('No rooms available for the selected dates. Please try a different room or date.')
        else:
            # Handle form invalid case
            return HttpResponse('Form data is not valid.')

class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('bookings:BookingListView')
