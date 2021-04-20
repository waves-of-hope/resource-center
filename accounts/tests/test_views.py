from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase

from accounts import views


class AccountsBaseTestCase(TestCase):
    """Sets up data to be shared across tests for accounts.views

    Args:
        TestCase (object): a subclass of django.test.TransactionTestCase
    """
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = get_user_model().objects.create_user(
            first_name='Alvin',
            email = 'alvin@mukuna.com',
            password = 'alvinpassword'
        )


class LoginViewTestCase(AccountsBaseTestCase):
    """Tests for the Login view

    Args:
        AccountsBaseTestCase (object): a subclass of django.test.TestCase
    """
    def test_login_view_basic(self):
        """Test that the login view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/accounts/login/')
        response = views.LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('accounts/login.html'):
            response.render()


class LogoutViewTestCase(AccountsBaseTestCase):
    """Tests for the Logout view

    Args:
        AccountsBaseTestCase (object): a subclass of django.test.TestCase
    """
    def test_redirect_if_not_logged_in(self):
        """
        Test that the logout view redirects to the home page
        when a user is not logged in
        """
        response = self.client.get('/accounts/logout/')
        self.assertRedirects(response, '/')

    def test_logout_redirect_url(self):
        """
        Test that the logout view redirects to the home page
        when a user is logged in
        """
        self.client.login(email = 'alvin@mukuna.com',
            password = 'alvinpassword'
        )
        response = self.client.get('/accounts/logout/')
        self.assertRedirects(response, '/')


class PasswordResetViewTestCase(AccountsBaseTestCase):
    """Tests for the PasswordReset view

    Args:
        AccountsBaseTestCase (object): a subclass of django.test.TestCase
    """
    def test_password_reset_view_basic(self):
        """Test that the password reset view returns a 200 response
        and uses the correct template
        """
        request = self.factory.get('/accounts/password_reset/')
        response = views.PasswordResetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('accounts/password_reset.html'):
            response.render()


class PasswordResetDoneViewTestCase(AccountsBaseTestCase):
    """Tests for the PasswordResetDone view

    Args:
        AccountsBaseTestCase (object): a subclass of django.test.TestCase
    """
    def test_password_reset_done_view_basic(self):
        """Test that the password reset done view returns
        a 200 response and uses the correct template
        """
        request = self.factory.get('/accounts/password_reset_done/')
        response = views.PasswordResetDoneView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('accounts/password_reset_done.html'):
            response.render()


class PasswordResetCompleteViewTestCase(AccountsBaseTestCase):
    """Tests for the PasswordResetComplete view

    Args:
        AccountsBaseTestCase (object): a subclass of django.test.TestCase
    """
    def test_password_reset_complete_view_basic(self):
        """Test that the password reset complete view returns
        a 200 response and uses the correct template
        """
        request = self.factory.get('/accounts/password_reset_complete/')
        response = views.PasswordResetCompleteView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('accounts/password_reset_complete.html'):
            response.render()


class ProfileViewTestCase(AccountsBaseTestCase):
    """Tests for the profile view

    Args:
        AccountsBaseTestCase (object): a subclass of django.test.TestCase
    """
    def test_redirect_if_not_logged_in(self):
        """Test that the profile view redirects to the login page first
        when a user is not logged in
        """
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
            '/accounts/login/?next=/accounts/profile/')

    def test_profile_view_logged_in_basic(self):
        """Test that the profile view returns a 200 response
        and uses the correct template when a user is logged in
        """
        self.client.login(email = 'alvin@mukuna.com',
            password = 'alvinpassword'
        )
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/profile.html')
        self.assertEqual(str(response.context['user']), 'Alvin')


class RegisterViewTestCase(AccountsBaseTestCase):
    """Tests for the register view

    Args:
        AccountsBaseTestCase (object): a subclass of django.test.TestCase
    """
    def test_register_view_basic(self):
        """Test that the register view returns a 200 response
        and uses the correct template
        """
        request = self.factory.get('/accounts/register/')
        with self.assertTemplateUsed('accounts/register.html'):
            response = views.register(request)
            self.assertEqual(response.status_code, 200)
