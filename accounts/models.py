from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractUser):
    """A custom user model

    Args:
        AbstractUser (object): A subclass of
            django.contrib.auth.models.AbstractBaseUser
    """
    username = None
    email = models.EmailField('email address',
        error_messages={'unique': 'A user with that email address already exists.'},
        unique=True
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField(max_length=20, help_text='Enter a valid phone number' )
    bio = models.TextField(max_length=1000, help_text='Enter a brief summary of yourself', null=True, blank=True)
    profile_picture = models.ImageField(default='default.png', upload_to='profile_pictures')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',]
    objects = UserManager()

    def __str__(self):
        return self.first_name
