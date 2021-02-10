import datetime

from django.utils import timezone

from selenium import webdriver

from .base import ResourceCenterTestCase
from resources.models import Category, Tag, Book, Video


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

        # Kelvin wants to add a record and a number of books
        # and videos to Waves Resource Center. He goes back to
        # the homepage of the admin site
        self.browser.find_element_by_css_selector(
            '#site-name a').click()

        # He clicks on Categories and sees all of the Categories
        # that have been added so far. They are ordered by name
        self.browser.find_element_by_link_text('Categories').click()
        category_rows = self.browser.find_elements_by_css_selector(
            '#result_list tr')

        self.assertEqual(category_rows[1].text, 'Agribusiness')
        self.assertEqual(category_rows[2].text, 'Finance')
        self.assertEqual(category_rows[3].text, 'Spiritual')

        # Each name is a link to the detail page of each category
        # where its details can be changed
        self.assertEqual(
            self.browser.find_element_by_link_text('Spiritual').\
                get_attribute('href'),
            self.live_server_url + '/admin/resources/'
                'category/1/change/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text('Agribusiness').\
                get_attribute('href'),
            self.live_server_url + '/admin/resources/'
                'category/2/change/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text('Finance').\
                get_attribute('href'),
            self.live_server_url + '/admin/resources/'
                'category/3/change/'
        )

        # Going back to the home page, he clicks the Tags link
        # and sees the Tags that have been added ordered by name.
        self.browser.find_element_by_css_selector(
            '#site-name a').click()
        self.browser.find_element_by_link_text('Tags').click()
        tag_rows = self.browser.find_elements_by_css_selector(
            '#result_list tr')

        self.assertEqual(tag_rows[1].text, 'Christian finance')
        self.assertEqual(tag_rows[2].text, 'Faith')
        self.assertEqual(tag_rows[3].text, 'Healing')
        self.assertEqual(tag_rows[4].text, 'Hydroponics')
        self.assertEqual(tag_rows[5].text, 'Love')
        self.assertEqual(tag_rows[6].text, 'Salvation')

        # Each name is a link to the detail page of each tag
        # where its details can be changed
        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Love').get_attribute('href'),
            self.live_server_url + '/admin/resources/'
                'tag/1/change/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Salvation').get_attribute('href'),
            self.live_server_url + '/admin/resources/'
                'tag/2/change/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Faith').get_attribute('href'),
            self.live_server_url + '/admin/resources/'
                'tag/3/change/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Healing').get_attribute('href'),
            self.live_server_url + '/admin/resources/'
                'tag/4/change/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Christian finance').get_attribute('href'),
            self.live_server_url + '/admin/resources/'
                'tag/5/change/'
        )

        self.assertEqual(
            self.browser.find_element_by_link_text(
                'Hydroponics').get_attribute('href'),
            self.live_server_url + '/admin/resources/'
                'tag/6/change/'
        )
