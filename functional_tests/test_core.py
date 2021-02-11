import datetime

from selenium import webdriver

from .base import ResourceCenterTestCase
from core.models import Category, Tag


class AdminTestCase(ResourceCenterTestCase):
    """Tests the functionality of the core features to superusers
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

    def test_that_an_admin_can_manage_categories_and_tags(self):
        """Tests that a staff can manage categories and tags
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

        # He sees links to CORE, Categories and Tags
        self.assertEqual(
            self.browser.\
                find_element_by_link_text('CORE').\
                    get_attribute('href'),
            self.live_server_url + '/admin/core/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Categories').\
                    get_attribute('href'),
            self.live_server_url + '/admin/core/category/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Tags').\
                    get_attribute('href'),
            self.live_server_url + '/admin/core/tag/'
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
        self.assertIsNotNone(
            self.browser.find_element_by_link_text('Spiritual').\
                get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text('Agribusiness').\
                get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text('Finance').\
                get_attribute('href')
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
        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'Love').get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'Salvation').get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'Faith').get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'Healing').get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'Christian finance').get_attribute('href')
        )

        self.assertIsNotNone(
            self.browser.find_element_by_link_text(
                'Hydroponics').get_attribute('href')
        )
