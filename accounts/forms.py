from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from hotel.models import Room

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

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username__iexact=username)  # Use your custom user model's manager
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('This username is already taken. Please choose another.')

class ChangeRoomStatusForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the form if needed (e.g., add extra widgets or queryset filtering)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email']