from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, EditProfileForm
from django.contrib.auth import authenticate, login
from .models import User, Guest, Staff
#from django.urls import reverse

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('accounts:login_view')
        else:
            msg = 'form is not valid'
    else:
        form = RegisterForm()
    return render(request,'register.html', {'form': form, 'msg': msg})

def edit_profile(request):
    user = request.user

    # Check if the user has the 'GUEST' role
    if user.role == User.Role.GUEST:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                # Redirect to a success page or back to the form
                return redirect('success_page')
        else:
            form = EditProfileForm(instance=user)

        return render(request, 'edit_profile.html', {'form': form})
    else:
        # Redirect to an unauthorized page or display a message
        return render(request, 'unauthorized.html')  # Create an unauthorized template
    
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
                
                # Check the role and redirect based on the role
                if user.role == User.Role.ADMIN:
                    return redirect('adminpage')
                elif user.role == User.Role.STAFF:
                    return redirect('staff')
                elif user.role == User.Role.GUEST:
                    return redirect('accounts:guestpls')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    
    return render(request, 'login.html', {'form': form, 'msg': msg})


def admin(request):
    return render(request,'admin.html')


def staff(request):
    return render(request,'staff.html')


def guestpls(request):
    return render(request,'guesttemp.html')

# In views.py
def test_view(request):
    return render(request, 'test.html')
