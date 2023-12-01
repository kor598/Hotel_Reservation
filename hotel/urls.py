from django.urls import path, include
from . import views
from .views import room_list_view

app_name="hotel"

urlpatterns = [
    path('room_list/', room_list_view, name="RoomListView"),
    # path('generate_standard_hotel/', views.generate_standard_hotel, name='generate_standard_hotel')
    #path('hotel_exists/', views.hotel_exists, name='hotel_exists'),
]