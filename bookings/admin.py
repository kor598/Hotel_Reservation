from django.contrib import admin
from bookings.models import Room, Booking

# Register your models here.
admin.site.register(Room)
admin.site.register(Booking)