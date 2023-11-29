from django.urls import path
from .views import index, login_view, register, admin, staff, guestpls, edit_profile, test_view

app_name = 'accounts'

urlpatterns = [
    path('', index, name= 'index'),
    path('login/', login_view, name='login_view'),
    path('register/', register, name='register'),
    path('adminpage/', admin, name='adminpage'),
    path('staff/', staff, name='staff'),
    path('guesttemp/', guestpls, name='guestpls'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    # In urls.py
    path('test/', test_view, name='test_view'),
]