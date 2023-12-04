from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Guest, Cleaner

# Custom admin class for User model
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
# Custom admin class for Guest model
class GuestAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')

# Custom admin class for Cleaner model
class CleanerAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'hotel_id')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'hotel__name')

# Register the models with their respective admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Cleaner, CleanerAdmin)
