from django.test import SimpleTestCase
from django.urls import resolve, reverse

from accounts import views

class AccountsURLsTestCase(SimpleTestCase):
    """
    Test URL configuration of accounts
    """
    def test_register_url(self):
        """
        Test that the URL for register resolves to the
        correct view function
        """
        register = resolve(reverse('register'))
        self.assertEqual(register.func, views.register)

    def test_profile_url(self):
        """
        Test that the URL for profile resolves to the
        correct view function
        """
        profile = resolve(reverse('profile'))
        self.assertEqual(profile.func, views.profile)

    def test_login_url(self):
        """
        Test that the URL for login resolves to the
        correct view function
        """
        login = resolve(reverse('login'))
        self.assertEqual(login.func.__name__, 'LoginView')

    def test_logout_url(self):
        """
        Test that the URL for logout resolves to the
        correct view function
        """
        login = resolve(reverse('logout'))
        self.assertEqual(login.func.__name__, 'LogoutView')

    def test_password_reset_url(self):
        """
        Test that the URL for password reset resolves to the
        correct view function
        """
        password_reset = resolve(reverse('password_reset'))
        self.assertEqual(password_reset.func.__name__,
            'PasswordResetView'
        )

    def test_password_reset_done_url(self):
        """
        Test that the URL for password reset done
        resolves to the correct view function
        """
        password_reset_done = resolve(
            reverse('password_reset_done')
        )
        self.assertEqual(
            password_reset_done.func.__name__,
            'PasswordResetDoneView'
        )

    def test_password_reset_complete_url(self):
        """
        Test that the URL for password reset complete
        resolves to the correct view function
        """
        password_reset_complete = resolve(
            reverse('password_reset_complete')
        )
        self.assertEqual(
            password_reset_complete.func.__name__,
            'PasswordResetCompleteView'
        )
