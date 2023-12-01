from django.urls import path, include
from . import views
from .views import room_list_view

app_name="hotel"

urlpatterns = [
    path('room_list/', room_list_view, name="RoomListView"),
]