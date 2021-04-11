from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTestCase(TestCase):
    """Tests for the custom user model manager

    Args:
        TestCase (object): A subclass of django.test.TransactionTestCase
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.User = get_user_model()

        # create a normal user
        cls.user = cls.User.objects.create_user(
            # first_name='Normal',
            # last_name='User',
            email='normal@user.com',
            # phone_number='+2540110234567',
            password='foo'
        )

        # create a superuser
        cls.superuser = cls.User.objects.create_superuser(
            email='super@user.com',
            password='foo'
        )

    def test_user_has_no_username(self):
        self.assertIsNone(self.user.username)
        self.assertIsNone(self.superuser.username)

    def test_user_can_not_be_created_without_all_required_fields(self):
        # Type Errors - null values
        with self.assertRaises(TypeError):
            self.User.objects.create_user()

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='test-normal@user.com'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(first_name='Normal')

        with self.assertRaises(TypeError):
            self.User.objects.create_user(last_name='User')

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                phone_number='+2540110234567'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(password='foo')

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='test-normal@user.com',
                first_name='Normal'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='test-normal@user.com',
                last_name='User'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='test-normal@user.com',
                phone_number='+2540110234567'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                first_name='Normal',
                last_name='User'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                first_name='Normal',
                phone_number='+2540110234567'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                first_name='Normal',
                password='foo'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                last_name='User',
                phone_number='+2540110234567'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                last_name='User',
                password='foo'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                phone_number='+2540110234567',
                password='foo'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='test-normal@user.com',
                first_name='Normal',
                last_name='User',
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='test-normal@user.com',
                first_name='Normal',
                phone_number='+2540110234567'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='test-normal@user.com',
                last_name='User',
                phone_number='+2540110234567'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                first_name='Normal',
                last_name='User',
                phone_number='+2540110234567'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                first_name='Normal',
                last_name='User',
                password='foo'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                first_name='Normal',
                phone_number='+2540110234567',
                password='foo'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                last_name='User',
                phone_number='+2540110234567',
                password='foo'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='test-normal@user.com',
                first_name='Normal',
                last_name='User',
                phone_number='+2540110234567',
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                first_name='Normal',
                last_name='User',
                phone_number='+2540110234567',
                password='foo'
            )

        # Value Errors - blank email
        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='',
                password='foo'
            )

        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='',
                first_name='Normal',
                password='foo'
            )

        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='',
                last_name='User',
                password='foo'
            )

        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='',
                phone_number='+2540110234567',
                password='foo'
            )

        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='',
                first_name='Normal',
                last_name='User',
                password='foo'
            )

        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='',
                first_name='Normal',
                phone_number='+2540110234567',
                password='foo'
            )

        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                email='',
                first_name='Normal',
                last_name='User',
                phone_number='+2540110234567',
                password='foo'
            )

    def test_superuser_can_not_be_created_without_all_required_fields(self):
        # not superuser
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='super@user.com',
                password='foo',
                is_superuser=False
                )

        # not staff
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='super@user.com',
                password='foo',
                is_staff=False
                )

        # Type Errors - null values
        with self.assertRaises(TypeError):
            self.User.objects.create_superuser()

        with self.assertRaises(TypeError):
            self.User.objects.create_superuser(
                email='test-super@user.com'
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_superuser(first_name='Super')

        with self.assertRaises(TypeError):
            self.User.objects.create_superuser(password='foo')

        with self.assertRaises(TypeError):
            self.User.objects.create_superuser(
                email='test-super@user.com',
                first_name='Super',
            )

        with self.assertRaises(TypeError):
            self.User.objects.create_superuser(
                first_name='Super',
                password='foo'
            )

        # Value Errors - blank
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(email='', password='foo')

        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email='',
                first_name='Super',
                password='foo'
            )
