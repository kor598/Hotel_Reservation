from django.urls import path, include
from . import views
from .views import RoomListView, RoomDetailView, BookingList, BookingForm

app_name="bookings"

urlpatterns = [
    path('room_list/', RoomListView.as_view(), name="RoomList"),
    path('booking_list/', BookingList.as_view(), name="BookingList"),
    path('book/', BookingForm.as_view(), name="BookingView"),
    path('room/<type>', RoomDetailView.as_view(), name="RoomDetailView"),
]