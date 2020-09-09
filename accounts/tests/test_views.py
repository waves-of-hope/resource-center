from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

from accounts import views

class AccountsBaseTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = get_user_model().objects.create_user(
            first_name = 'Alvin',
            last_name = 'Mukuna',
            email = 'alvin@mukuna.com',
            phone_number = '+254 701 234 567',
            password = 'alvinpassword'
        )


class RegisterViewTestCase(AccountsBaseTestCase):
    
    def test_register_view_basic(self):
        """
        Test that register view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/accounts/register/')
        with self.assertTemplateUsed('accounts/register.html'):
            response = views.register(request)
            self.assertEqual(response.status_code, 200)


class ProfileViewTestCase(AccountsBaseTestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/accounts/profile')
        self.assertEqual(response.status_code, 301)

    def test_logged_in_uses_correct_template(self):
        self.client.login(email = 'alvin@mukuna.com',
            password = 'alvinpassword'
        )
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/profile.html')
        self.assertEqual(str(response.context['user']), 'Alvin')


class LoginViewTestCase(AccountsBaseTestCase):
    
    def test_login_view_basic(self):
        """
        Test that the login view returns a 200 response and
        uses the correct template
        """
        request = self.factory.get('/accounts/login/')
        response = views.LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('accounts/login.html'):
            response.render()


class LogoutViewTestCase(AccountsBaseTestCase):

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/accounts/logout')
        self.assertEqual(response.status_code, 301)

    def test_logged_in_uses_correct_template(self):
        self.client.login(email = 'alvin@mukuna.com',
            password = 'alvinpassword'
        )
        with self.assertTemplateUsed('accounts/logout.html'):
            response = self.client.get('/accounts/logout/')
            self.assertEqual(response.status_code, 200)


class PasswordResetViewTestCase(AccountsBaseTestCase):
    
    def test_password_reset_view_basic(self):
        """
        Test that the password reset view returns a 200 response
        and uses the correct template
        """
        request = self.factory.get('/accounts/password_reset/')
        response = views.PasswordResetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('accounts/password_reset.html'):
            response.render()


class PasswordResetDoneViewTestCase(AccountsBaseTestCase):
    
    def test_password_reset_done_view_basic(self):
        """
        Test that the password reset done view returns 
        a 200 response and uses the correct template
        """
        request = self.factory.get('/accounts/password_reset_done/')
        response = views.PasswordResetDoneView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('accounts/password_reset_done.html'):
            response.render()


class PasswordResetCompleteViewTestCase(AccountsBaseTestCase):
    
    def test_password_reset_complete_view_basic(self):
        """
        Test that the password reset complete view returns 
        a 200 response and uses the correct template
        """
        request = self.factory.get('/accounts/password_reset_complete/')
        response = views.PasswordResetCompleteView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('accounts/password_reset_complete.html'):
            response.render()
