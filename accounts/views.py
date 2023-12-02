from django.shortcuts import render, redirect
from .forms import LoginForm, GuestRegisterForm, CustomUserChangeForm
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib.auth.views import LogoutView

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

                staff_group = Group.objects.filter(name='Staff').first()
                guests_group = Group.objects.filter(name='Guests').first()
                #Redirecting users based on groups
                if staff_group and staff_group in user.groups.all():
                    return redirect('staff')
                elif guests_group and guests_group in user.groups.all():
                    return redirect('accounts:guestpls')
                elif user.is_staff or user.is_superuser:
                    return redirect('admin:index')
                else:
                    msg = 'User does not belong to any recognized group.'
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'

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
    
def staff(request):
    return render(request,'staff.html')

def guestpls(request):
    return render(request,'guesttemp.html')

def test_view(request):
    return render(request, 'test.html')
