from django.urls import path, include
from . import views
from .views import RoomList, BookingList, BookingForm

app_name="bookings"

urlpatterns = [
    path('room_list/', RoomList.as_view(), name="RoomList"),
    path('booking_list/', BookingList.as_view(), name="BookingList"),
    path('booking_view/', BookingForm.as_view(), name="booking_view"),
]