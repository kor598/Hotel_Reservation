from django.urls import include, path, reverse_lazy
from .views import index, login_view, guest_register, cleaners_view, guestpls, CustomLogoutView, update_profile, CustomPasswordResetView, update_room_status
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('', index, name= 'index'),
    path('login/', login_view, name='login_view'),
    path('register/', guest_register, name='guest_register'),
    path('cleaners/', cleaners_view, name='cleaners_view'),
    path('guesttemp/', guestpls, name='guestpls'),
    path('logout/', CustomLogoutView.as_view(), name='custom_logout'),
    path('update-profile/', update_profile, name='update_profile'),
    path('update_room_status/<int:room_id>/', update_room_status, name='update_room_status'),
    
    path('password_reset/', CustomPasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='password_reset_confirm.html',
    success_url=reverse_lazy('accounts:password_reset_complete')
), name='password_reset_confirm'),


    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]