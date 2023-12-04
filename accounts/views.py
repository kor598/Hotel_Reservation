from django.shortcuts import render, redirect
from .forms import LoginForm, GuestRegisterForm, CustomUserChangeForm, ChangeRoomStatusForm
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth.views import LogoutView, PasswordResetView
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from hotel.models import HotelRoom
from hotel.room_status import RoomStatus
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')


def guest_register(request):
    msg = None
    if request.method == 'POST':
        form = GuestRegisterForm(request.POST)
        if form.is_valid():
            # Instead of calling form.save(), use your custom method
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Assuming you have password fields in your form

            # Call the create_guest method
            user = User.objects.create_guest(email=email, username=username, password=password)

            msg = 'user created'
            return redirect('accounts:login_view')
        else:
            msg = 'form is not valid'
    else:
        form = GuestRegisterForm()

    return render(request, 'register.html', {'form': form, 'msg': msg})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                cleaner_group = Group.objects.filter(name='Cleaners').first()
                guests_group = Group.objects.filter(name='Guests').first()
                #Redirecting users based on groups
                if cleaner_group  in user.groups.all():
                    return redirect('accounts:cleaners_view')
                elif guests_group in user.groups.all():
                    return redirect('accounts:guestpls')
                elif user.is_staff or user.is_superuser:
                    return redirect('admin:index')
                else:
                    msg = 'User does not belong to any recognized group.'
            else:
                # Check if the user exists but the password is incorrect
                user_exists = authenticate(username=username, password='')
                if user_exists:
                    msg = 'Incorrect password.\nNote: Staff and Admin must reset password on first login.'
        else:
            msg = 'Invalid username'
    else:
        msg = 'Error validating form'
    if msg:
        msg = msg.replace('\n', '<br>')
    return render(request, 'login.html', {'form': form, 'msg': msg})

def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:guestpls')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        #check logout has occured
        super().get(request, *args, **kwargs)
        # Redirect to login page
        return redirect('accounts:login_view')

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        # Check if the user with the provided email or username exists
        email = form.cleaned_data['email']  # Assuming your form has an 'email' field
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            messages.success(self.request, 'Password reset email sent successfully.')
            return super().form_valid(form)
        else:
            # User is not in the database, show an error message
            messages.error(self.request, 'User not found. Please check your email or username.')
            return super().form_invalid(form)

def cleaners_view(request):
    # Get all checked-out rooms
    checked_out_rooms = HotelRoom.objects.filter(room__room_status=RoomStatus.CHECKED_OUT.value)
    print(checked_out_rooms)
    if request.method == 'POST':
        # Check if the form is valid (you need to create the form in your forms.py)
        form = ChangeRoomStatusForm(request.POST)
        if form.is_valid():
            # Get the selected room from the form
            selected_room = form.cleaned_data['room']

            # Use the clean_room function to change the status
            selected_room.room.clean_room()

            # Redirect to the same view to update the room list
            return redirect('cleaners_view')

    else:
        form = ChangeRoomStatusForm()

    context = {'checked_out_rooms': checked_out_rooms, 'form': form}
    return render(request, 'cleaners.html', context)

def guestpls(request):
    return render(request,'guesttemp.html')

def test_view(request):
    return render(request, 'test.html')
