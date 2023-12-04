from django.urls import path, include
from . import views
from .views import room_list_view, choose_hotel_view

app_name="hotel"

urlpatterns = [
    path('room_list/<int:hotel_id>/', room_list_view, name="RoomListView"),
    path('book/', choose_hotel_view, name='choose_hotel'),
    # path('generate_standard_hotel/', views.generate_standard_hotel, name='generate_standard_hotel')
    #path('hotel_exists/', views.hotel_exists, name='hotel_exists'),
]