from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    """
    A custom user model that extends AbstractUser to
    support addition of more fields
    """
    phone_number = PhoneNumberField(
        max_length=20, 
        help_text='Enter a valid phone number'
    )

    bio = models.TextField(
        max_length=1000,
        help_text='Enter a brief summary of yourself',
        null=True,
        blank=True
    )

    profile_picture = models.ImageField(default='default.png',
        upload_to="profile_pictures"    
    )


    def __str__(self):
        return self.username
