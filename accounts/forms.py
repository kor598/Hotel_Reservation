from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from hotel.models import Room

#custom login form
class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
#form for registering guests, only works for guests as view assigns to groups guests and is_staff is set to false
class GuestRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    #for checking username is unique
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username__iexact=username) 
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('This username is already taken. Please choose another.')

class ChangeRoomStatusForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#for editing user details
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email']