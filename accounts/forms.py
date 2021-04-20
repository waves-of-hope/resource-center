from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'bio', 'profile_picture')

