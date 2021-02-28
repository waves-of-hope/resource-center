import datetime

from django.utils import timezone

from selenium import webdriver

from .base import ResourceCenterTestCase
from core.models import Category, Tag
from books.models import Book
import utils.test

class BooksTestCase(ResourceCenterTestCase):
    """Sets up data to be shared across tests for the books feature

    Args:
        ResourceCenterTestCase (object): A subclass of
        django.contrib.staticfiles.testing.StaticLiveServerTestCase
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


class AdminTestCase(BooksTestCase):
    """Test the functionality of the books feature to superusers
    and users with staff permissions

    Args:
        BooksTestCase (object): A subclass of ResourceCenterTestCase
    """
    def test_that_a_staff_can_manage_books(self):
        """Tests that a staff can manage books
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

        # He sees links to CORE, Categories, Tags and Books
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

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('BOOKS').\
                    get_attribute('href'),
            self.live_server_url + '/admin/books/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Books').\
                    get_attribute('href'),
            self.live_server_url + '/admin/books/book/'
        )

        # Kelvin wants to add a record and a number of books to Waves
        # Resource Center. He goes back to the root of the admin site
        # and clicks on 'Books'
        self.browser.find_element_by_css_selector(
            '#site-name a').click()
        self.browser.find_element_by_link_text('Books').click()

        # He's sees the title, Category and Tags of each book
        # listed with the latest books first
        book_rows = self.browser.find_elements_by_css_selector('#result_list tr')

        self.assertEqual(book_rows[1].text,
            'The Gift Spiritual Faith, Healing, Love ...')
        self.assertEqual(book_rows[2].text,
            'The Hydroponics handbook Agribusiness Hydroponics')
        self.assertEqual(book_rows[3].text,
            'A Christian\'s guide to wealth creation Spiritual Christian finance')

        # He adds a Book to a Category, Tag and User
        # that already exists
        self.browser.find_element_by_link_text('ADD BOOK').click()
        book_form = self.browser.find_element_by_id('book_form')

        book_form.find_element_by_name('title').\
            send_keys('Divine Healing')
        book_form.find_element_by_name('authors').\
            find_elements_by_tag_name('option')[3].click()
        book_form.find_element_by_name('summary').\
            send_keys('Outlines how to claim divine healing '
            'that is available to us by faith')
        book_form.find_element_by_name('category').\
            find_elements_by_tag_name('option')[3].click()

        tags_to_choose = [1,2]
        for tag in tags_to_choose:
            book_form.find_element_by_name('tags').\
                find_elements_by_tag_name('option')[tag].click()
        book_form.find_element_by_css_selector(
            'input#id_cover_image').send_keys(
                utils.test.get_absolute_file_path('images/book-cover.jpg'))
        book_form.find_element_by_css_selector(
            'input#id_file_upload').send_keys(
                utils.test.get_absolute_file_path('documents/book.pdf'))
        book_form.find_element_by_css_selector(
            '.submit-row input').click()

        import time; time.sleep(2)
        book_rows = self.browser.find_elements_by_css_selector(
                '#result_list tr')

        self.assertGreater(len(book_rows), 1)

        # TODO: fails in CI
        self.assertEqual(
            book_rows[1].text,
            'Divine Healing Spiritual Faith, Healing'
        )

        # He then adds a Book for which the Category, Tags and
        # Author do not yet exist
        add_book_link = self.browser.find_element_by_link_text('ADD BOOK')
        add_book_link.click()

        # He adds a Category from the Book page
        book_form = self.browser.find_element_by_id('book_form')
        book_form.find_element_by_id('add_id_category').click()
        self.browser.switch_to.window(self.browser.window_handles[1])

        category_form = self.browser.find_element_by_id('category_form')
        category_form.find_element_by_name('name').\
            send_keys('Technology')
        category_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He adds some Tags from the Book page
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.find_element_by_id('book_form').\
            find_element_by_id('add_id_tags').click()

        self.browser.switch_to.window(self.browser.window_handles[1])
        tag_form = self.browser.find_element_by_id('tag_form')
        tag_form.find_element_by_name('name').\
            send_keys('Programming')
        tag_form.find_element_by_css_selector(
            '.submit-row input').click()

        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.find_element_by_id('book_form').\
            find_element_by_id('add_id_tags').click()

        self.browser.switch_to.window(self.browser.window_handles[1])
        tag_form = self.browser.find_element_by_id('tag_form')
        tag_form.find_element_by_name('name').\
            send_keys('Python')
        tag_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He adds an Author from the Book page
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.find_element_by_id('book_form').\
            find_element_by_id('add_id_authors').click()

        self.browser.switch_to.window(self.browser.window_handles[1])
        user_form = self.browser.find_element_by_id('user_form')
        user_form.find_element_by_css_selector(
            'input#id_first_name').send_keys('Karen')
        user_form.find_element_by_css_selector(
            'input#id_last_name').send_keys('Wangui')
        user_form.find_element_by_css_selector(
            'input#id_email').send_keys('karen@wangui.com')
        user_form.find_element_by_css_selector(
            'input#id_phone_number').send_keys('+254 756 789 012')
        user_form.find_element_by_css_selector(
            'input#id_password1').send_keys('karenpassword')
        user_form.find_element_by_css_selector(
            'input#id_password2').send_keys('karenpassword')
        user_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He adds the Book's details and saves it
        self.browser.switch_to.window(self.browser.window_handles[0])
        book_form = self.browser.find_element_by_id('book_form')
        book_form.find_element_by_name('title').\
            send_keys('Getting started with programming in Python')
        book_form.find_element_by_css_selector(
            'input#id_cover_image').send_keys(
                utils.test.get_absolute_file_path('images/book-cover.jpg'))
        book_form.find_element_by_css_selector(
            'input#id_file_upload').send_keys(
                utils.test.get_absolute_file_path('documents/book.pdf'))
        book_form.find_element_by_css_selector(
            '.submit-row input').click()

        self.assertEqual(
            self.browser.find_elements_by_css_selector(
                '#result_list tr')[1].text,
            'Getting started with programming in Python '
            'Technology Programming, Python'
        )


class MemberTestCase(BooksTestCase):
    """Tests the functionality of the books feature to members
    and unregistered users

    Args:
        BooksTestCase (object): A subclass of ResourceCenterTestCase
    """
    def test_that_a_user_can_read_or_download_books(self):
        """Tests that a user can see the books list page and read
        or download books in the detail pages
        """
        # Alex would like to read Christian books and watch sermons
        # to grow Spiritually. He has been hearing about Waves
        # Resource Center from his friends. He visits the home page
        # of Waves Resource Center.
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
        # the register and login pages.
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
        register_form = self.browser.find_element_by_id('register_form')
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

        # He is redirected to the login page, where he sees the inputs
        # of the login form, including labels and placeholders
        login_form = self.browser.find_element_by_id('login_form')
        self.assertEqual(login_form.\
                find_element_by_css_selector('legend').text,
            'Login'
        )

        email_input = login_form.find_element_by_css_selector(
            'input#id_username')
        self.assertEqual(
            login_form.find_element_by_css_selector(
                'label[for="id_username"]').text,
            'Email address*'
        )

        password_input = login_form.find_element_by_css_selector(
            'input#id_password')
        self.assertEqual(
            login_form.find_element_by_css_selector(
                'label[for="id_password"]').text,
            'Password*'
        )

        # He enters his email and password and clicks the login button
        # to log in to the resource center.
        email_input.send_keys('alex@githinji.com')
        password_input.send_keys('alexpassword')
        login_form.find_element_by_css_selector(
            'button[type="submit"]').click()

        # The login was successful and he is redirected to the books
        # list page, where he finds some books.
        self.assertEqual(
            self.browser.current_url,
            '{}/books/'.format(self.live_server_url)
        )

        books = self.browser.\
            find_elements_by_css_selector('.book-card')
        self.assertGreater(len(books), 0)

        # The books list page is paginated
        # TODO: reduce complexity
        pagination = self.browser.find_element_by_css_selector(
            'nav ul.pagination')
        page_links, page_link_addresses = list(), list()
        for i in range(7):
            if i == 0:
                page_links.append('Previous')
                page_link_addresses.append('/books/#')
            elif i == 7:
                page_links.append('Next')
            else:
                page_link_addresses.append('/books/?page={}/'.\
                    format(i))

        for i, link in enumerate(page_links):
            self.assertEqual(pagination.find_element_by_link_text(
                    page_links[i]).get_attribute('href'),
                self.live_server_url + page_link_addresses[i]
            )

        # He clicks on the first book and is taken to the book's
        # detail page which has a link to download the book.
        books[0].find_element_by_css_selector(
            '.card-title a').click()
        self.assertEqual(
            self.browser.current_url,
            '{}/books/the-gift/'.format(self.live_server_url)
        )

        self.assertEqual(
            self.browser.find_element_by_css_selector(
                '.card-title').text,
            'The Gift'
        )

        m2m_attributes = self.browser.find_elements_by_css_selector(
            '.m2m-attribute')
        tags = m2m_attributes[0].\
            find_elements_by_css_selector('a.btn')
        self.assertEqual(tags[0].text, 'faith')
        self.assertEqual(tags[1].text, 'healing')
        self.assertEqual(tags[2].text, 'love')
        self.assertEqual(tags[3].text, 'salvation')

        authors = m2m_attributes[1].\
            find_elements_by_css_selector('a')
        self.assertEqual(authors[0].text, 'Kelvin')
        self.assertEqual(authors[1].text, 'Christine')

        # TODO: fails in CI
        import time; time.sleep(2)
        download_link = self.browser.find_element_by_link_text(
            'Download The Gift (13.0 KB)')
        self.assertEqual(
            download_link.get_attribute('href'),
            '{}/media/book.pdf'.format(
                self.live_server_url)
        )
