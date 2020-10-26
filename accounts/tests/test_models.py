from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTestCase(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.User = get_user_model()

        # create a normal user
        cls.user = cls.User.objects.create_user(
            first_name='Normal',
            last_name='User',
            email='normal@user.com',
            phone_number='+2540110234567',
            password='foo'
        )

        # create a superuser
        cls.admin_user = cls.User.objects.create_superuser(
            email='super@user.com',
            password='foo'
        )

    def test_normal_user_basic(self):
        """
        Test the basic functionality of non-superuser
        """
        self.assertEqual(self.user.first_name, 'Normal')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.email, 'normal@user.com')
        self.assertEqual(self.user.phone_number, '+2540110234567')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_superuser_basic(self):
        """
        Test the basic functionality of superuser
        """
        self.assertEqual(self.admin_user.email, 'super@user.com')
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

    def test_user_object_name(self):
        """
        Test the name of the User object that will
        be shown in django admin
        """
        self.assertEqual(self.user.first_name, str(self.user))
    
    def test_email_meta(self):
        """
        Test meta attributes of the the email field
        """
        email__meta = self.user._meta.get_field('email')
        self.assertEqual(email__meta.verbose_name, 'email address')
        self.assertEqual(email__meta.null, False)
        self.assertEqual(email__meta.blank, False)

    def test_first_name_meta(self):
        """
        Test meta attributes of the the first name field
        """
        first_name__meta = self.user._meta.get_field('first_name')
        self.assertEqual(first_name__meta.verbose_name, 'first name')
        self.assertEqual(first_name__meta.max_length, 30)
        self.assertEqual(first_name__meta.null, False)
        self.assertEqual(first_name__meta.blank, False)

    def test_last_name_meta(self):
        """
        Test meta attributes of the the last name field
        """
        last_name__meta = self.user._meta.get_field('last_name')
        self.assertEqual(last_name__meta.verbose_name, 'last name')
        self.assertEqual(last_name__meta.max_length, 30)
        self.assertEqual(last_name__meta.null, False)
        self.assertEqual(last_name__meta.blank, False)

    def test_phone_number_meta(self):
        """
        Test meta attributes of the phone number field
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
        self.assertEqual(phone_number__meta.null, False)
        self.assertEqual(phone_number__meta.blank, False)

    def test_bio_meta(self):
        """
        Test meta attributes of the bio field
        """
        bio__meta = self.user._meta.get_field('bio')
        self.assertEqual(bio__meta.verbose_name, 'bio')
        self.assertEqual(bio__meta.max_length, 1000)
        self.assertEqual(bio__meta.help_text, 
            'Enter a brief summary of yourself'
        )
        self.assertEqual(bio__meta.null, True)
        self.assertEqual(bio__meta.blank, True)

    def test_profile_picture_meta(self):
        """
        Test meta attributes of the profile picture field
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
        self.assertEqual(profile_picture__meta.null, False)
        self.assertEqual(profile_picture__meta.blank, False)

    def test_create_user(self):
        """
        Test creation of a normal user account
        """
        self.assertIsNone(self.user.username)
        
        # Type Errors - missing email or password
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
        
        # Value Errors - missing data in email
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
                last_name='User',
                phone_number='+2540110234567',
                password='foo'
            )

    def test_create_superuser(self):
        """
        Test creation of a superuser account
        """
        self.assertIsNone(self.admin_user.username)

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
        
        # Type Errors - missing email or password
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

        # Value Errors - missing data in email        
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(email='', password='foo')
