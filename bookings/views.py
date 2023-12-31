from datetime import datetime, time
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils import timezone
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy

from hotel.room_status import RoomStatus
from .forms import AvailabilityForm

from bookings.booking_functions.availability import check_availability
from bookings.booking_functions.get_available_rooms import get_available_rooms
from bookings.booking_functions.book_room import book_room

from hotel.room_functions.get_room_type import get_room_type

from bookings.models import Booking
from hotel.models import CheckedInState, CheckedOutState, Room

from django.views.generic import DeleteView

# Create your views here.
class CheckInView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, 'check_in_success.html', {'room': room})
    
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        
        room_bookings = Booking.objects.filter(room=room)
        
        if not room_bookings:
            return HttpResponseBadRequest("No bookings found for this room.")
        
        current_date = timezone.now().date()
        current_time = timezone.now().time()
        check_in_time = time(16, 0, 0)  # 4 PM set check-in time
        
        matching_booking = room_bookings.filter(check_in_date__date=current_date).first()
        
        if not matching_booking:
            return HttpResponseBadRequest("Cannot check in: This booking is not for today.")
        elif matching_booking.check_in_date.time() < check_in_time:
            return HttpResponseBadRequest("Cannot check in: Check-in time is before 4 PM.")
        
        if room.room_status != RoomStatus.CLEANED.value:
            return HttpResponseBadRequest("Cannot check in: Room is not clean. Please contact a staff member.")
        
        if room.room_status == RoomStatus.CHECKED_IN.value:
            return HttpResponseBadRequest("You've already checked in!")
        
        # Perform the check-in state transition
        checked_in_state = CheckedInState()
        points_earned = checked_in_state.handle(room)
        
        if points_earned is not None:
            # Assuming successful check-in scenario where points are earned
            room.save()
            return render(request, 'check_in_success.html', {'room': room, 'points_earned': points_earned})
        else:
            # Handle error scenario where no booking is found for today
            return HttpResponseBadRequest("Error: No booking found for today.")

# check out view
class CheckOutView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, 'check_out_success.html', {'room': room})
    
    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        

        checked_out_state = CheckedOutState()
        checked_out_state.handle(room) 

        room.save()
        return render(request, 'check_out_success.html', {'room': room})


# booking list view. shows bookings
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
        room_type = self.kwargs.get('type', None)
        room_type_name = get_room_type(room_type)
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
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            check_in_time = data['check_in_date']
            check_out_time = data['check_out_date']

            # Set the time to 4:00 PM for both check-in and check-out
            check_in_time = check_in_time.replace(hour=16, minute=0, second=0)
            check_out_time = check_out_time.replace(hour=16, minute=0, second=0)

            if check_in_time.date() < timezone.now().date():
                return HttpResponse('Check-in date cannot be in the past.')

            if check_out_time <= check_in_time:
                return HttpResponse('Check-out date should be after the check-in date.')

            available_rooms = get_available_rooms(room_type, check_in_time, check_out_time)

            if available_rooms:
                booking = book_room(request, available_rooms[0], check_in_time, check_out_time)

                formatted_check_in = check_in_time.strftime("%Y-%m-%d %H:%M:%S")
                formatted_check_out = check_out_time.strftime("%Y-%m-%d %H:%M:%S")

                context = {
                    'room_type': room_type,
                    'check_in': formatted_check_in,
                    'check_out': formatted_check_out,
                    'nights_stay': booking.nights_of_stay(),
                    'total_price': booking.apply_discount(),
                    'points_earned': booking.calculate_points_earned(),
                    'points_used': booking.calculate_points_deducted(),
                }

                # messages.success(
                #     self.request,
                #     f'Your booking for a {room_type} room from {formatted_check_in} to {formatted_check_out} has been confirmed! Thank you for choosing us.'
                # )

                # Fetch the hotel ID dynamically from the booked room or replace it with the correct logic
                hotel_id = None
                if booking and booking.room and booking.room.hotel:
                    hotel_id = booking.room.hotel.id

                if hotel_id:
                    room_list_url = reverse('hotel:RoomListView', args=[hotel_id])
                    return redirect('paypal-payment', booking_id=booking.id)
                    # return HttpResponseRedirect(room_list_url)
                else:
                    return HttpResponse('Hotel not found!')
            else:
                return HttpResponse('No rooms available for the selected dates. Please try a different room or date.')
        else:
            return HttpResponse('Form data is not valid.')

# booking confirmation view      
        
class BookingConfirmationView(View):
    def get(self, request, room_id):
        booking = Booking.objects.get(pk=room_id)

        context = {
            'room_type': booking.get_room_type(),
            'check_in': booking.check_in_date,
            'check_out': booking.check_out_date,
            'nights_stay': booking.nights_of_stay(),
            'total_price': booking.calculate_price(),
            'points_earned': booking.calculate_points_earned(),
            'points_used': booking.calculate_points_deducted(),
        }
        
        print(context)
        print(booking.__dict__)

        return render(request, 'booking_confirmation.html', context)

# booking cancel view
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('bookings:BookingListView')
