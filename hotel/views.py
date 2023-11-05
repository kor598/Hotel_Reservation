from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from hotelReservation import settings
from django.core.mail import send_mail
from django.views.generic import ListView, FormView
from .models import Room, Booking
from .forms import AvailabilityForm
from hotel.booking_functions.availability import check_availability

# temp view to see rooms
class RoomList(ListView):
    model = Room

class BookingList(ListView):
    model = Booking
    
class BookingForm(FormView):
    form_class = AvailabilityForm
    template_name = 'hotel/availability_form.html'
    
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



# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        #check if username is already used
        if User.objects.filter(username=username):
            messages.error(request, "username already exists")
            return redirect('home')
        
        #check if email is alredy registered
        if User.objects.filter(email=email):
            messages.error(request, "email already exists")
            return redirect('home')
        
        #check if username is under 10 characters
        if len(username)>10:
            messages.error(request, "username must be under 10 characters")
            
        #check if passwords match
        if pass1 != pass2:
            messages.error(request, "passwords don't match")
            
        #check if username is alphanumeric
        if not username.isalnum():
            messages.error(request, "username must be alphanumeric")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, "Your Account has been successfully created.")
        
        return redirect('signin')
    
    
    return render(request, "authentication/signup.html")

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        #if the user is authenticated
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
            
        #if the user is not authenticated    
        else:
            messages.error(request, "Bad Credentials")
            return redirect('home')
    
    #checks passowrd of the user in the database
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

