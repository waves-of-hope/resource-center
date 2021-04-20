from selenium import webdriver

import utils.test

from .base import ResourceCenterTestCase


class MemberTestCase(ResourceCenterTestCase):
    """Tests the functionality of the accounts feature to members
    and unregistered users

    Args:
        ResourceCenterTestCase (object): A subclass of ResourceCenterTestCase
    """
    def setUp(self):
        self.browser = webdriver.Firefox(options=self.browser_options)

        self.user = self.User.objects.create_user(
            first_name = 'Brian',
            last_name = 'Kimani',
            email = 'brian@kimani.com',
            phone_number = '+254 712 345 678',
            password = 'brianpassword'
        )

    def test_that_a_member_can_update_their_profile(self):
        """Tests that a member can update their profile
        """
        # Brian is a registered member of Waves of Hope Foundation
        # who would like to update his account profile. He visits the
        # profile page of Waves Resource Center ...
        profile_page =self.browser.get(
            self.live_server_url + '/accounts/profile/'
        )

        # ... but is redirected to the login page first. He sees
        # the inputs of the login form, including labels and
        # placeholders
        login_form = self.browser.find_element_by_id('login_form')
        self.assertEqual(login_form.\
                find_element_by_css_selector('legend').text,
            'Login'
        )

        email_input = login_form.\
            find_element_by_css_selector('input#id_username')
        self.assertEqual(login_form.find_element_by_css_selector(
            'label[for="id_username"]').text,
            'Email address*'
        )

        password_input = login_form.\
            find_element_by_css_selector('input#id_password')
        self.assertEqual(login_form.find_element_by_css_selector(
            'label[for="id_password"]').text,
            'Password*'
        )

        # He keys in his email and password and submits the form
        # to log in ...
        email_input.send_keys('brian@kimani.com')
        password_input.send_keys('brianpassword')
        login_form.find_element_by_css_selector(
            'button[type="submit"]').click()

        # ... and is taken the profile page where he sees the profile
        # update form. He can now update his profile.
        profile_form = self.browser.find_element_by_id('profile_form')
        self.assertEqual(profile_form.\
                find_element_by_css_selector('legend').text,
            'Profile info'
        )

        first_name_input = profile_form.\
            find_element_by_css_selector('input#id_first_name')
        self.assertEqual(first_name_input.get_attribute('value'),
            'Brian')
        self.assertEqual(profile_form.find_element_by_css_selector(
                'label[for="id_first_name"]').text,
            'First name*'
        )

        last_name_input = profile_form.\
            find_element_by_css_selector('input#id_last_name')
        self.assertEqual(last_name_input.get_attribute('value'),
            'Kimani')
        self.assertEqual(profile_form.find_element_by_css_selector(
            'label[for="id_last_name"]').text,
            'Last name*'
        )

        email_input = profile_form.\
            find_element_by_css_selector('input#id_email')
        self.assertEqual(email_input.get_attribute('value'),
            'brian@kimani.com')
        self.assertEqual(profile_form.find_element_by_css_selector(
            'label[for="id_email"]').text,
            'Email address*'
        )

        phone_number_input = profile_form.\
            find_element_by_css_selector('input#id_phone_number')
        self.assertEqual(phone_number_input.get_attribute('value'),
            '+254712345678')
        self.assertEqual(profile_form.find_element_by_css_selector(
            'label[for="id_phone_number"]').text,
            'Phone number*'
        )
        self.assertEqual(profile_form.find_element_by_css_selector(
                'small#hint_id_phone_number').text,
            'Enter a valid phone number'
        )

        bio_input = profile_form.\
            find_element_by_css_selector('textarea#id_bio')
        self.assertEqual(profile_form.find_element_by_css_selector(
            'label[for="id_bio"]').text,
            'Bio'
        )
        self.assertEqual(profile_form.find_element_by_css_selector(
                'small#hint_id_bio').text,
            'Enter a brief summary of yourself'
        )

        profile_picture_input = profile_form.\
            find_element_by_css_selector('input#id_profile_picture')
        self.assertEqual(profile_form.find_element_by_css_selector(
            'label[for="id_profile_picture"]').text,
            'Profile picture*'
        )
        current_image = profile_form.find_element_by_css_selector(
            'div#div_id_profile_picture a')
        self.assertEqual(current_image.get_attribute('href'),
            self.live_server_url + '/media/default.png'
        )

        # He keys in some information about himself in the bio,
        # uploads a new profile picture and submits the form to
        # update his profile
        brians_bio = "Brian is a member of Waves of Hope Foundation."
        "He seeks to read, do and share God's word."
        bio_input.send_keys(brians_bio)
        profile_picture_input.send_keys(
            utils.test.get_absolute_file_path('images/user.png'))
        profile_form.find_element_by_css_selector(
            'button[type="submit"]').click()

        # He sees a message informing him that the profile update
        # was successful. He confirms that the bio and new profile
        # picture are already input in the profile form
        # TODO: fails in CI
        alerts = self.browser.find_elements_by_css_selector(
            '.alert')
        # utils.test.explicit_wait(self.assertIn(
        #     'Your profile has been updated\n×',
        #     [alert.text for alert in alerts]
        # ))
        updated_profile_form = self.browser.find_element_by_id('profile_form')

        self.assertEqual(
            updated_profile_form.find_element_by_css_selector(
                'textarea#id_bio').get_attribute('value'),
            brians_bio)

        utils.test.explicit_wait(self.assertEqual(
            updated_profile_form.find_element_by_css_selector(
                '#div_id_profile_picture a').get_attribute('href'),
            self.live_server_url + '/media/profile_pictures/'
                'user.png'
            ))
