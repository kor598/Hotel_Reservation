from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import ListView, FormView, View
from .forms import AvailabilityForm
from bookings.availability import check_availability
from bookings.models import Room, Booking
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User

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
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)
                
        if len(available_rooms) > 0:        
            room = available_rooms[0]
            guest_users = User.objects.filter(role=User.Role.GUEST)  
            if guest_users.exists():
                guest_user = guest_users.first()
                
                booking = Booking.objects.create(
                    user = guest_user,
                    room = room,
                    check_in = data['check_in'],
                    check_out = data['check_out']
            )        
            booking.save()
            messages.success(self.request, f'Your booking for {room} from {data["check_in"]} to {data["check_out"]} has been confirmed!! Thank you for choosing us.')
            return HttpResponse(booking)
        else:
            return HttpResponse('No rooms available for the selected dates. Please try a different room or date.')
    
class BookingForm(LoginRequiredMixin, FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(room_type=data['room_type'])
        available_rooms = [room for room in room_list if check_availability(room, data['check_in'], data['check_out'])]

        if available_rooms:
            room = available_rooms[0]

            # Fetch the 'Guest' user from User model
            guest_users = User.objects.filter(role=User.Role.GUEST)  
            if guest_users.exists():
                guest_user = guest_users.first()

                booking = Booking.objects.create(
                    user=guest_user,  # Associate booking with the 'Guest' user
                    room=room,
                    check_in=data['check_in'],
                    check_out=data['check_out']
                )
                booking.save()

                messages.success(
                    self.request,
                    f'Your booking for {room} from {data["check_in"]} to {data["check_out"]} has been confirmed!! Thank you for choosing us.'
                )
                return HttpResponse('Booking created for guest user!')
            else:
                return HttpResponse('No users of type "Guest" found. Cannot create booking.')
        else:
            return HttpResponse('No rooms available for the selected dates. Please try a different room or date.')