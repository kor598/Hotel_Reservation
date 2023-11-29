from django.urls import path, include
from . import views
from .views import RoomListView, RoomDetailView, BookingListView, CancelBookingView

app_name="bookings"

urlpatterns = [
    path('room_list/', RoomListView, name="RoomListView"),
    path('booking_list/', BookingListView.as_view(), name="BookingListView"),
    # path('book/', BookingForm.as_view(), name="BookingView"),
    path('room/<type>/', RoomDetailView.as_view(), name="RoomDetailView"),
    path('booking/cancel/<pk>/', CancelBookingView.as_view(), name="CancelBookingView"),
]