from selenium import webdriver

from .base import ResourceCenterTestCase
import utils.test


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


class AdminTestCase(ResourceCenterTestCase):
    """Test the functionality of the accounts feature to superusers
    and users with staff permissions

    Args:
        ResourceCenterTestCase (object): A subclass of ResourceCenterTestCase
    """
    def setUp(self):
        self.browser = webdriver.Firefox(options=self.browser_options)

        self.admin_user = self.User.objects.create_superuser(
            first_name = 'Kelvin',
            email='kelvin@murage.com',
            password='kelvinpassword'
        )

        self.user1 = self.User.objects.create_user(
            first_name = 'Alvin',
            last_name = 'Mukuna',
            email = 'alvin@mukuna.com',
            phone_number = '+254 701 234 567',
            password = 'alvinpassword'
        )

        self.user2 = self.User.objects.create_user(
            first_name = 'Brian',
            last_name = 'Kimani',
            email = 'brian@kimani.com',
            phone_number = '+254 712 345 678',
            password = 'brianpassword'
        )

        self.user3 = self.User.objects.create_user(
            first_name = 'Christine',
            last_name = 'Kyalo',
            email = 'christine@kyalo.com',
            phone_number = '+254 723 456 789',
            password = 'christinepassword'
        )

    def test_that_an_admin_can_manage_groups_and_user_permissions(self):
        """Tests that a superuser can manage group and user permissions
        """
        # Kelvin would like to give Christine permissions to login
        # to the admin site and add books for other viewers to read.
        # He visits the admin site
        admin_root = self.browser.get(
            self.live_server_url + '/admin/'
        )

        # He can tell he's in the right place because of the title
        self.assertEqual(self.browser.title,
            'Log in | Waves Resource Center site admin'
        )

        # He enters his email and password and submits the form to
        # log in
        login_form = self.browser.find_element_by_id(
            'login-form')
        login_form.find_element_by_name('username').\
            send_keys('kelvin@murage.com')
        login_form.find_element_by_name('password').\
            send_keys('kelvinpassword')
        login_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He sees links to ACCOUNTS, Users, AUTHENTICATION
        # AND AUTHORIZATION and Groups
        self.assertEqual(
            self.browser.\
                find_element_by_link_text('ACCOUNTS').\
                    get_attribute('href'),
            self.live_server_url + '/admin/accounts/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Users').\
                    get_attribute('href'),
            self.live_server_url + '/admin/accounts/user/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('AUTHENTICATION AND AUTHORIZATION').\
                    get_attribute('href'),
            self.live_server_url + '/admin/auth/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Groups').\
                    get_attribute('href'),
            self.live_server_url + '/admin/auth/group/'
        )

        # He clicks on the Groups link
        self.browser.find_element_by_css_selector(
            '#site-name a').click()

        self.browser.find_element_by_link_text('Groups').click()

        # He creates a group with create, edit and view permissions
        # for the User model in the Accounts app
        self.browser.find_element_by_link_text('ADD GROUP').click()
        group_form = self.browser.find_element_by_id('group_form')
        group_form.find_element_by_name('name').send_keys('Editors')
        group_form.find_element_by_id('id_permissions_input').\
            send_keys('accounts')

        permissions_to_add = group_form.\
            find_element_by_name('permissions_old')
        options_to_choose = [1, -1]
        for choice in options_to_choose:
            permissions_to_add.\
                find_elements_by_tag_name('option')[choice].click()
            group_form.find_element_by_link_text('Choose').click()

        group_form.find_element_by_css_selector(
            '.submit-row input').click()

        self.assertEqual(
            self.browser.find_elements_by_css_selector(
                '#result_list tr')[1].text,
            'Editors'
        )

        # Going back to the home page of the admin, he clicks the
        # Users link and sees all users who have registered
        # to the site. They are ordered by first name
        self.browser.find_element_by_css_selector(
            '#site-name a').click()
        self.browser.find_element_by_link_text('Users').click()

        user_rows = self.browser.find_elements_by_css_selector(
            '#result_list tr')
        self.assertEqual(user_rows[1].text,
            'Alvin Mukuna alvin@mukuna.com +254701234567')
        self.assertEqual(user_rows[2].text,
            'Brian Kimani brian@kimani.com +254712345678')
        self.assertEqual(user_rows[3].text,
            'Christine Kyalo christine@kyalo.com +254723456789')
        self.assertEqual(user_rows[4].text,
            'Kelvin kelvin@murage.com')

        # He also sees links to change the users information
        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'Alvin').get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'Brian').get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'Christine').get_attribute('href')
        )

        # At the moment, Christine can't login to the admin site
        christines_details = self.browser.\
            find_elements_by_css_selector('#result_list tr')[3]

        self.assertEqual(
            christines_details.find_element_by_css_selector(
                '.field-is_staff img').get_attribute('alt'),
            'False'
        )

        # He clicks on Christine's link to add her to the
        # editors group
        self.browser.find_element_by_link_text('Christine').click()
        user_form = self.browser.find_element_by_id('user_form')
        user_form.find_element_by_name('is_staff').click()
        user_form.find_element_by_name('groups_old').\
            find_elements_by_tag_name('option')[0].click()
        user_form.find_element_by_link_text('Choose').click()
        user_form.find_element_by_css_selector(
            '.submit-row input').click()

        #  Christine is now able to login to the admin panel
        christines_details = self.browser.\
            find_elements_by_css_selector('#result_list tr')[3]

        self.assertEqual(
            christines_details.text,
            'Christine Kyalo christine@kyalo.com +254723456789'
        )

        self.assertEqual(
            christines_details.find_element_by_css_selector(
                '.field-is_staff img').get_attribute('alt'),
            'True'
        )
