from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Guest, User
from hotel.models import Room

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
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
    email = forms.EmailField(
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
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Guest
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number']


def clean_email(self):
        email = self.cleaned_data['email']
        # Normalize the email (convert to lowercase) before checking for uniqueness
        email = email.lower()
        try:
            User.objects.get(email__iexact=email)  # Use your custom user model's manager
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email is already taken. Please choose another.')

class ChangeRoomStatusForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Guest
        fields = ['email', 'first_name', 'last_name', 'phone_number']