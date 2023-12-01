from django.urls import include, path
from .views import index, login_view, guest_register, staff, guestpls

app_name = 'accounts'

urlpatterns = [
    path('', index, name= 'index'),
    path('login/', login_view, name='login_view'),
    path('register/', guest_register, name='guest_register'),
    path('staff/', staff, name='staff'),
    path('guesttemp/', guestpls, name='guestpls'),
]