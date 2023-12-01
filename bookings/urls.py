from django.urls import path 
from .views import RoomDetailView, BookingListView, CancelBookingView, CheckInView, CheckOutView

app_name="bookings"

urlpatterns = [
    path('booking_list/', BookingListView.as_view(), name="BookingListView"),
    # path('book/', BookingForm.as_view(), name="BookingView"),
    path('room/<type>/', RoomDetailView.as_view(), name="RoomDetailView"),
    path('booking/cancel/<pk>/', CancelBookingView.as_view(), name="CancelBookingView"),
    path('booking/check_in/<int:room_id>/', CheckInView.as_view(), name="CheckInView"),
    path('booking/check_out/<int:room_id>/', CheckOutView.as_view(), name="CheckOutView"),
]