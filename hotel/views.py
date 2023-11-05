from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from hotelReservation import settings
from django.core.mail import send_mail

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