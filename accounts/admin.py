from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        if obj.role in [User.Role.STAFF, User.Role.ADMIN] and request.user.role != User.Role.ADMIN:
            raise Exception("Only admins can create or update staff/admin users.")
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
