from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()

        # create a normal user
        self.user = self.User.objects.create_user(
            username='normal-user',
            email='normal@user.com',
            phone_number='+2540110234567',
            password='foo'
            )

        # create a superuser
        self.admin_user = self.User.objects.create_superuser(
            username='super-user',
            email='super@user.com',
            password='foo'
            )

    def test_normal_user_basic(self):
        """
        Test the basic functionality of non-superuser
        """
        self.assertEqual(self.user.username, 'normal-user')
        self.assertEqual(self.user.email, 'normal@user.com')
        self.assertEqual(self.user.phone_number, '+2540110234567')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_superuser_basic(self):
        """
        Test the basic functionality of superuser
        """
        self.assertEqual(self.admin_user.username, 'super-user')
        self.assertEqual(self.admin_user.email, 'super@user.com')
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

    def test_object_name(self):
        """
        Test the name of the User object that will
        be shown in django admin
        """
        self.assertEqual(self.user.username, str(self.user))
    
    def test_phone_number_meta(self):
        """
        Test meta attributes of phone number field
        """
        phone_number__meta = self.user._meta.\
            get_field('phone_number')
        self.assertEqual(phone_number__meta.verbose_name,
            'phone number'
        )
        self.assertEqual(phone_number__meta.max_length, 20)
        self.assertEqual(phone_number__meta.help_text,
            'Enter a valid phone number'
        )

    def test_bio_meta(self):
        """
        Test meta attributes of bio field
        """
        bio__meta = self.user._meta.get_field('bio')
        self.assertEqual(bio__meta.verbose_name, 'bio')
        self.assertEqual(bio__meta.max_length, 1000)
        self.assertEqual(bio__meta.help_text, 
            'Enter a brief summary of yourself'
        )

    def test_profile_picture_meta(self):
        """
        Test meta attributes of profile picture field
        """
        profile_picture__meta = self.user._meta.\
            get_field('profile_picture')
        self.assertEqual(profile_picture__meta.verbose_name,
            'profile picture'
        )
        self.assertEqual(profile_picture__meta.default,
            'default.png'
        )
        self.assertEqual(profile_picture__meta.upload_to,
            'profile_pictures'
        )

    def test_create_user(self):
        """
        Test creation of a normal user account
        """
        # Type Errors - missing username
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
               
        with self.assertRaises(TypeError):
            self.User.objects.create_user(email='normal@user.com')
        
        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                phone_number='+2540110234567'
            )
        
        with self.assertRaises(TypeError):
            self.User.objects.create_user(password='foo')
        
        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='normal@user.com',
                password='foo'
            )
        
        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='normal@user.com',
                phone_number='+2540110234567'
            )
        
        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                phone_number='+2540110234567',
                password='foo'
            )
        
        with self.assertRaises(TypeError):
            self.User.objects.create_user(
                email='normal@user.com',
                phone_number='+2540110234567',
                password='foo'
            )

        # Value Errors - missing data in username
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='')
        
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='',
                email='normal@user.com'
            )
        
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='',
                phone_number='+2540110234567'
            )
        
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='',
                password='foo'
            )
        
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='',
                email='normal@user.com',
                phone_number='+2540110234567'
            )
        
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='',
                email='normal@user.com', password='foo'
            )
        
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='',
                phone_number='+2540110234567', password='foo'
            )


    def test_create_superuser(self):
        """
        Test creation of a superuser account
        """
        # not superuser
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                username='super-user',
                email='super@user.com',
                password='foo',
                is_superuser=False
                )
        
        # Type Errors - missing username
        with self.assertRaises(TypeError):
            self.User.objects.create_superuser()
               
        with self.assertRaises(TypeError):
            self.User.objects.create_superuser(
                email='super@user.com'
            )
        
        with self.assertRaises(TypeError):
            self.User.objects.create_superuser(password='foo')
        
        with self.assertRaises(TypeError):
            self.User.objects.create_superuser(
                email='super@user.com',
                password='foo'
            )

        # Value Errors - missing data in username
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(username='')
        
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(username='',
                email='super@user.com'
            )
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(username='',
                password='foo'
            )
        
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(username='',
                email='super@user.com',
                password='foo'
            )
