from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('staff/', views.staff, name='staff'),
    path('guest/', views.guest, name='guest'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
