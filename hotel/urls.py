from django.contrib import admin
from django.urls import path, include
from . import views
from .views import RoomList, BookingList, BookingForm

app_nhame="hotel"

urlpatterns = [
   path('', views.home, name="home"),
   path('signup', views.signup, name="signup"),
   path('signin', views.signin, name="signin"),
   path('signout', views.signout, name="signout"),
   path('room_list/', RoomList.as_view(), name="RoomList"),
   path('booking_list/', BookingList.as_view(), name="BookingList"),
   path('booking_view/', BookingForm.as_view(), name="booking_view"),
]