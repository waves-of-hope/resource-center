from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """A custom user model manager

    Args:
        BaseUserManager (object): Provides methods for creating a user
        and superuser for a custom user model with fields not similar to
        Django's default user
    """
    def create_user(self, email, password, **extra_fields):
        """Creates a normal user account with the given email and
        password plus any other attributes

        Args:
            email (str): An email address
            password (str): A password

        Raises:
            ValueError: If an email address isn't provided

        Returns:
            object: An instance of the User model
        """
        if not email:
            raise ValueError('Email address must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates a superuser account with the given email and password

        Args:
            email (str): An email address
            password (str): A password

        Raises:
            ValueError: If the is_staff flag is not set to True
            ValueError: If the is_superuser flag is not set to True

        Returns:
            object: An instance of the User model
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
