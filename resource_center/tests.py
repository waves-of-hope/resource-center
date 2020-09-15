from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase, tag, override_settings

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import os
from pathlib import WindowsPath
from shutil import rmtree
from .settings import BASE_DIR

@tag('functional')
@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
@override_settings(MEDIA_ROOT=BASE_DIR / 'test_media')
class ResourceCenterTestCase(LiveServerTestCase):

    def setUp(self):
        # set up test media directory
        self.MEDIA_ROOT = BASE_DIR / 'test_media'
        self.MEDIA_ROOT.mkdir()

        # directory for getting files for upload
        self.TEST_FILES = BASE_DIR / 'test_files'

        # set up browser in GitHub runner
        if os.getenv('SELENIUM_JAR_PATH'):
            options = Options()
            options.add_argument('-headless')
            self.browser = webdriver.Firefox(
                executable_path='geckodriver',
                options=options
            )
            self.browser.implicitly_wait(2)

        else:
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(2)

        # create some test users
        self.User = get_user_model()

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

    def tearDown(self):
        self.browser.quit()
        rmtree(self.MEDIA_ROOT)

    def test_member_can_find_resources(self):
        """
        Test that a member can find resources,
        i.e: books and videos
        """
        # Alex is a member of Waves of Hope Foundation who would
        # like to read Christian books and watch sermons to grow
        # Spiritually. He visits the home page of Waves Resource
        # Center.
        home_page =self.browser.get(self.live_server_url + '/')

        # He knows he's in the right place because he can see the
        # name of the site in the navbar, as well as calls-to-action
        # in the heading and adjacent paragraph.
        self.assertEqual(
            self.browser.find_element_by_css_selector(
                '.navbar-brand').text,
            'Waves Resource Center'
        )

        self.assertEqual(
            self.browser.find_element_by_css_selector('h1').text,
            'Be Empowered Today For Free',
        )

        self.assertEqual(self.browser.\
                find_element_by_css_selector('h1 + p').text,
            'Find books, videos and opportunities that will '
                'change your life forever',
        )

        # He sees two call-to-action buttons, which are links for
        #  the register and login pages.
        cta_buttons =self.browser.\
            find_elements_by_css_selector('.homepage-cta a.btn')
        self.assertEqual(len(cta_buttons), 2)

        register_link, login_link = cta_buttons
        self.assertEqual('Register', register_link.text)
        self.assertEqual('Login', login_link.text)
        self.assertEqual(register_link.get_attribute('href'),
            self.live_server_url + '/accounts/register/'
        )
        self.assertEqual(login_link.get_attribute('href'),
            self.live_server_url + '/accounts/login/'
        )

        # He doesn't have an account and therefore decides to
        # register. He clinks on the register link and is redirected
        # to the register page, where he sees the inputs of the
        # register form, including labels and placeholders.
        register_link.click()
        register_form = self.browser.\
            find_element_by_id('register_form')
        self.assertEqual(register_form.\
                find_element_by_css_selector('legend').text,
            'Register'
        )

        first_name_input = register_form.\
            find_element_by_css_selector('input#id_first_name')
        self.assertEqual(register_form.find_element_by_css_selector(
                'label[for="id_first_name"]').text,
            'First name*'
        )

        last_name_input = register_form.\
            find_element_by_css_selector('input#id_last_name')
        self.assertEqual(register_form.find_element_by_css_selector(
            'label[for="id_last_name"]').text,
            'Last name*'
        )

        email_input = register_form.\
            find_element_by_css_selector('input#id_email')
        self.assertEqual(register_form.find_element_by_css_selector(
            'label[for="id_email"]').text,
            'Email address*'
        )

        phone_number_input = register_form.\
            find_element_by_css_selector('input#id_phone_number')
        self.assertEqual(register_form.find_element_by_css_selector(
            'label[for="id_phone_number"]').text,
            'Phone number*'
        )
        self.assertEqual(register_form.find_element_by_css_selector(
                'small#hint_id_phone_number').text,
            'Enter a valid phone number'
        )

        password_input = register_form.\
            find_element_by_css_selector('input#id_password1')
        self.assertEqual(register_form.find_element_by_css_selector(
            'label[for="id_password1"]').text,
            'Password*'
        )
        password_input_help_text_list = register_form.\
            find_elements_by_css_selector('small#hint_id_password1 li')
        self.assertEqual(len(password_input_help_text_list), 4)

        password_confirmation_input = register_form.\
            find_element_by_css_selector('input#id_password2')
        self.assertEqual(register_form.find_element_by_css_selector(
                'label[for="id_password2"]').text,
            'Password confirmation*'
        )

        register_button = register_form.\
            find_element_by_css_selector('button[type="submit"]')
        self.assertEqual(register_button.text, 'Register')
        
        # He keys in his first name, last name, email, phone number
        # and password and clicks register button to send the form.
        first_name_input.send_keys('Alexander')
        last_name_input.send_keys('Githinji')
        email_input.send_keys('alex@githinji.com')
        phone_number_input.send_keys('+254 745 678 901')
        password_input.send_keys('alexpassword')
        password_confirmation_input.send_keys('alexpassword')
        register_form.find_element_by_css_selector(
            'button[type="submit"]').click()

        # The registration was successful, and he is redirected to
        # the login page where he sees the inputs of the login form,
        # including labels and placeholders
        login_form = self.browser.\
            find_element_by_id('login_form')
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

        # He enters his email and password and clicks the login button
        # to log in to the resource center.
        email_input.send_keys('alex@githinji.com')
        password_input.send_keys('alexpassword')
        login_form.find_element_by_css_selector(
            'button[type="submit"]').click()
        
        # self.fail('Incomplete Test')

        # The login was successful and he is redirected to the books
        # list page, where he finds some books. The books authors and
        # cover images are indicated together with the titles.

        # The books also have categories and tags which one can use to view
        #  resources in a particular area of interest.

        # He clicks on a book with a category of Spiritual ...

        # ... and is taken to the book's detail page which has a link
        # to download the book.

        # He clicks on the link and gets a copy of the e-book, 
        # which he starts reading.

    def test_member_can_update_profile(self):
        """
        Test that a member can update their profile
        """
        # Brian is a registered member of Waves of Hope Foundation
        # who would like to update his account profile. He visits the
        # login page of Waves Resource Center since he already has an
        # account and is not logged in.
        home_page =self.browser.get(
            self.live_server_url + '/accounts/login/'
        )

        # He sees the inputs of the login form, including labels
        # and placeholders
        login_form = self.browser.\
            find_element_by_id('login_form')
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
        # to log in.
        email_input.send_keys('brian@kimani.com')
        password_input.send_keys('brianpassword')
        login_form.find_element_by_css_selector(
            'button[type="submit"]').click()

        # He sees some links in the navbar ...
        navbar = self.browser.\
            find_element_by_css_selector('.navbar')
        
        self.assertEqual(
            navbar.\
                find_element_by_link_text('Books').\
                    get_attribute('href'),
            self.live_server_url + '/accounts/profile/#'
        )

        self.assertEqual(
            navbar.\
                find_element_by_link_text('Videos').\
                    get_attribute('href'),
            self.live_server_url + '/accounts/profile/#'
        )

        self.assertEqual(
            navbar.\
                find_element_by_link_text('Reports').\
                    get_attribute('href'),
            self.live_server_url + '/accounts/profile/#'
        )

        self.assertEqual(
            navbar.\
                find_element_by_link_text('Events').\
                    get_attribute('href'),
            self.live_server_url + '/accounts/profile/#'
        )

        self.assertEqual(
            navbar.\
                find_element_by_link_text('Gallery').\
                    get_attribute('href'),
            self.live_server_url + '/accounts/profile/#'
        )

        account_link = navbar.\
            find_element_by_link_text("Brian's Account")
        self.assertEqual(
            account_link.get_attribute('href'),
            self.live_server_url + '/accounts/profile/#'
        )

        # ... and finds the account link. He clicks it to reveal a
        # dropdown menu with some links for account related tasks
        account_link.click()

        account_menu = self.browser.\
            find_element_by_css_selector('.dropdown-menu')

        self.assertEqual(
            account_menu.\
                find_element_by_link_text('Logout').\
                    get_attribute('href'),
            self.live_server_url + '/accounts/logout/'
        )

        self.assertEqual(
            account_menu.\
                find_element_by_link_text('Profile').\
                    get_attribute('href'),
            self.live_server_url + '/accounts/profile/'
        )

        # He clicks on profile, which redirects him to the account
        # profile page. He sees the inputs of the profile form,
        # including labels and placeholders. He also sees the
        # information that he input when creating an account and
        # the default profile picture already filled out in the form
        account_menu.find_element_by_link_text('Profile').click()
        profile_form = self.browser.\
            find_element_by_id('profile_form')
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

        image_path =  self.TEST_FILES / 'images' / 'default.jpg'
        image_path_str = str(image_path.as_posix())
        if isinstance(image_path, WindowsPath):
            image_path_str = image_path_str.replace('/', '\\')        
        profile_picture_input.send_keys(image_path_str)
        profile_form.find_element_by_css_selector(
            'button[type="submit"]').click()

        # He sees a message informing him that the profile update
        # was successful. He confirms that the bio and new profile
        # picture are already input in the profile form
        self.assertEqual(
            self.browser.find_element_by_css_selector('.alert').text[:-2],
            'Your profile has been updated'
        )
        updated_profile_form = self.browser.\
            find_element_by_id('profile_form')
        
        self.assertEqual(
            updated_profile_form.find_element_by_css_selector(
                'textarea#id_bio').get_attribute('value'),
            brians_bio)

        self.assertEqual(
            updated_profile_form.find_element_by_css_selector(
                'div#div_id_profile_picture a').get_attribute('href'),
            self.live_server_url + '/media/profile_pictures/'
                'default.jpg'
            )

    def test_admin_can_manage_users(self):
        """
        Tests that a 'superuser' user can access the admin
        and give other users permissions
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

        # He sees links to Accounts, Users, Authentication
        #  and Authorization and Groups
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
        options_to_choose = [0, 0, 1]        
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
        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Alvin').get_attribute('href'),
            self.live_server_url + '/admin/accounts/user/2/change/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Brian').get_attribute('href'),
            self.live_server_url + '/admin/accounts/user/3/change/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Christine').get_attribute('href'),
            self.live_server_url + '/admin/accounts/user/4/change/'
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
