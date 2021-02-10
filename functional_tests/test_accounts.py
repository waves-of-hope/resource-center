import datetime

from django.utils import timezone

from selenium import webdriver

from .base import ResourceCenterTestCase
from resources.models import Category, Tag, Book, Video


class MemberTestCase(ResourceCenterTestCase):
    """
    Test the functionality of the Resource Center to members
    and unregistered users
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

        self.category1 = Category.objects.create(
            name='Spiritual',
            slug='spiritual'
        )

        self.category2 = Category.objects.create(
            name='Agribusiness',
            description='Tips and tricks to improve your farm',
            slug='agribusiness'
        )

        self.category3 = Category.objects.create(
            name='Finance',
            slug='finance'
        )

        self.tag1 = Tag.objects.create(
            name='Love',
            slug='love'
        )

        self.tag2 = Tag.objects.create(
            name='Salvation',
            slug='salvation'
        )

        self.tag3 = Tag.objects.create(
            name='Faith',
            slug='faith'
        )

        self.tag4 = Tag.objects.create(
            name='Healing',
            slug='healing'
        )

        self.tag5 = Tag.objects.create(
            name='Christian finance',
            slug='christian-finance'
        )

        self.tag6 = Tag.objects.create(
            name='Hydroponics',
            slug='hydroponics'
        )

        self.book1 = Book.objects.create(
            title='A Christian\'s guide to wealth creation',
            summary='A step-by-step guide on how to handle money'
                'as God has instructed in His Word',
            category=self.category1,
            slug='a-christians-guide-to-wealth-creation',
            file_upload='book.pdf',
            date_posted=timezone.now() - datetime.timedelta(days=2)
        )
        self.book1.authors.add(self.admin_user, self.user1,
            self.user2, self.user3)
        self.book1.tags.add(self.tag5)

        self.book2 = Book.objects.create(
            title='The Hydroponics handbook',
            summary='A guide to get started in Hydroponics '
                'with little capital',
            category=self.category2,
            slug='the-hydroponics-handbook',
            cover_image='book-cover.jpg',
            file_upload='book.pdf',
            date_posted=timezone.now() - datetime.timedelta(days=1)
        )
        self.book2.authors.add(self.admin_user)
        self.book2.tags.add(self.tag6)

        self.book3 = Book.objects.create(
            title='The Gift',
            summary='Explains why and how to recieve God\'s '
                'free gift of salvation',
            category=self.category1,
            slug='the-gift',
            file_upload='book.pdf'
        )
        self.book3.authors.add(self.admin_user, self.user3)
        self.book3.tags.add(self.tag1, self.tag2,
            self.tag3, self.tag4)

        # Create 20 books for pagination tests
        number_of_books = 20
        for i in range(number_of_books):
            prayer_devotion = Book.objects.create(
                title='Prayer Devotion {}'.format(i),
                category=self.category1,
                slug='prayer-devotion-{}'.format(i),
                cover_image='book-cover.jpg',
                file_upload='book.pdf',
                date_posted=timezone.now() - datetime.timedelta(days=3+i)
            )
            prayer_devotion.authors.add(self.admin_user)

        self.video1 = Video.objects.create(
            title='A Christian\'s guide to wealth creation',
            summary='A step-by-step guide on how to handle money'
                'as God has instructed in His Word',
            category=self.category1,
            slug='a-christians-guide-to-wealth-creation',
            url='https://youtu.be/rAKLiE658m0',
            date_posted=timezone.now() - datetime.timedelta(days=2)
        )
        self.video1.authors.add(self.admin_user, self.user1,
            self.user2, self.user3)
        self.video1.tags.add(self.tag5)

        self.video2 = Video.objects.create(
            title='The Hydroponics handbook',
            summary='A guide to get started in Hydroponics '
                'with little capital',
            category=self.category2,
            slug='the-hydroponics-handbook',
            url='https://youtu.be/rAKLiE658m0',
            date_posted=timezone.now() - datetime.timedelta(days=1)
        )
        self.video2.authors.add(self.admin_user)
        self.video2.tags.add(self.tag6)

        self.video3 = Video.objects.create(
            title='The Gift',
            summary='Explains why and how to recieve God\'s '
                'free gift of salvation',
            category=self.category1,
            slug='the-gift',
            url='https://youtu.be/rAKLiE658m0'
        )
        self.video3.authors.add(self.admin_user, self.user3)
        self.video3.tags.add(self.tag1, self.tag2,
            self.tag3, self.tag4)

        # Create 30 videos for pagination tests
        number_of_videos = 30
        for i in range(number_of_videos):
            the_gift_chapter = Video.objects.create(
                title='The Gift Chapter {}'.format(i),
                category=self.category1,
                slug='the-gift-chapter-{}'.format(i),
                url='https://youtu.be/rAKLiE658m0',
                date_posted=timezone.now() - datetime.timedelta(days=3+i)
            )
            the_gift_chapter.authors.add(self.admin_user)


    def test_member_can_update_profile(self):
        """
        Test that a member can update their profile
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
        # to log in ...
        email_input.send_keys('brian@kimani.com')
        password_input.send_keys('brianpassword')
        login_form.find_element_by_css_selector(
            'button[type="submit"]').click()

        # ... and is taken the profile page where he sees the profile
        # update form. He can now update his profile.
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
        profile_picture_input.send_keys(
            self.get_abs_test_file_path('images/user.png'))
        profile_form.find_element_by_css_selector(
            'button[type="submit"]').click()

        # He sees a message informing him that the profile update
        # was successful. He confirms that the bio and new profile
        # picture are already input in the profile form
        self.assertEqual(self.browser.find_elements_by_css_selector(
            '.alert')[0].text[:-2],
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
                'user.png'
            )


class AdminTestCase(ResourceCenterTestCase):
    """
    Test the functionality of the Resource Center to superusers
    and users with staff permissions
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

        self.category1 = Category.objects.create(
            name='Spiritual',
            slug='spiritual'
        )

        self.category2 = Category.objects.create(
            name='Agribusiness',
            description='Tips and tricks to improve your farm',
            slug='agribusiness'
        )

        self.category3 = Category.objects.create(
            name='Finance',
            slug='finance'
        )

        self.tag1 = Tag.objects.create(
            name='Love',
            slug='love'
        )

        self.tag2 = Tag.objects.create(
            name='Salvation',
            slug='salvation'
        )

        self.tag3 = Tag.objects.create(
            name='Faith',
            slug='faith'
        )

        self.tag4 = Tag.objects.create(
            name='Healing',
            slug='healing'
        )

        self.tag5 = Tag.objects.create(
            name='Christian finance',
            slug='christian-finance'
        )

        self.tag6 = Tag.objects.create(
            name='Hydroponics',
            slug='hydroponics'
        )

        self.book1 = Book.objects.create(
            title='A Christian\'s guide to wealth creation',
            summary='A step-by-step guide on how to handle money'
                'as God has instructed in His Word',
            category=self.category1,
            slug='a-christians-guide-to-wealth-creation',
            file_upload='book.pdf',
            date_posted=timezone.now() - datetime.timedelta(days=2)
        )
        self.book1.authors.add(self.admin_user, self.user1,
            self.user2, self.user3)
        self.book1.tags.add(self.tag5)

        self.book2 = Book.objects.create(
            title='The Hydroponics handbook',
            summary='A guide to get started in Hydroponics '
                'with little capital',
            category=self.category2,
            slug='the-hydroponics-handbook',
            cover_image='book-cover.jpg',
            file_upload='book.pdf',
            date_posted=timezone.now() - datetime.timedelta(days=1)
        )
        self.book2.authors.add(self.admin_user)
        self.book2.tags.add(self.tag6)

        self.book3 = Book.objects.create(
            title='The Gift',
            summary='Explains why and how to recieve God\'s '
                'free gift of salvation',
            category=self.category1,
            slug='the-gift',
            file_upload='book.pdf'
        )
        self.book3.authors.add(self.admin_user, self.user3)
        self.book3.tags.add(self.tag1, self.tag2,
            self.tag3, self.tag4)

        # Create 20 books for pagination tests
        number_of_books = 20
        for i in range(number_of_books):
            prayer_devotion = Book.objects.create(
                title='Prayer Devotion {}'.format(i),
                category=self.category1,
                slug='prayer-devotion-{}'.format(i),
                cover_image='book-cover.jpg',
                file_upload='book.pdf',
                date_posted=timezone.now() - datetime.timedelta(days=3+i)
            )
            prayer_devotion.authors.add(self.admin_user)

        self.video1 = Video.objects.create(
            title='A Christian\'s guide to wealth creation',
            summary='A step-by-step guide on how to handle money'
                'as God has instructed in His Word',
            category=self.category1,
            slug='a-christians-guide-to-wealth-creation',
            url='https://youtu.be/rAKLiE658m0',
            date_posted=timezone.now() - datetime.timedelta(days=2)
        )
        self.video1.authors.add(self.admin_user, self.user1,
            self.user2, self.user3)
        self.video1.tags.add(self.tag5)

        self.video2 = Video.objects.create(
            title='The Hydroponics handbook',
            summary='A guide to get started in Hydroponics '
                'with little capital',
            category=self.category2,
            slug='the-hydroponics-handbook',
            url='https://youtu.be/rAKLiE658m0',
            date_posted=timezone.now() - datetime.timedelta(days=1)
        )
        self.video2.authors.add(self.admin_user)
        self.video2.tags.add(self.tag6)

        self.video3 = Video.objects.create(
            title='The Gift',
            summary='Explains why and how to recieve God\'s '
                'free gift of salvation',
            category=self.category1,
            slug='the-gift',
            url='https://youtu.be/rAKLiE658m0'
        )
        self.video3.authors.add(self.admin_user, self.user3)
        self.video3.tags.add(self.tag1, self.tag2,
            self.tag3, self.tag4)

        # Create 30 videos for pagination tests
        number_of_videos = 30
        for i in range(number_of_videos):
            the_gift_chapter = Video.objects.create(
                title='The Gift Chapter {}'.format(i),
                category=self.category1,
                slug='the-gift-chapter-{}'.format(i),
                url='https://youtu.be/rAKLiE658m0',
                date_posted=timezone.now() - datetime.timedelta(days=3+i)
            )
            the_gift_chapter.authors.add(self.admin_user)


    def test_superuser_can_manage_users_and_content(self):
        """
        Tests that a 'superuser' user can access the admin manage
        the resource center's content and users.
        """
        # Kelvin would like to view categories and tags in the
        # resource center. He visits the admin site
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

        # He sees links to RESOURCES, Categories,
        # Tags and Videos
        self.assertEqual(
            self.browser.\
                find_element_by_link_text('RESOURCES').\
                    get_attribute('href'),
            self.live_server_url + '/admin/resources/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Categories').\
                    get_attribute('href'),
            self.live_server_url + '/admin/resources/category/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Tags').\
                    get_attribute('href'),
            self.live_server_url + '/admin/resources/tag/'
        )

    def test_superuser_can_manage_users_and_content(self):
        """
        Tests that a 'superuser' user can access the admin manage
        the resource center's content and users.
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
        # AND AUTHORIZATION, Groups, RESOURCES, Categories,
        # Tags, Books and Videos
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
