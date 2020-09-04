from django.test import tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


@tag('functional')
class MemberTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_member_find_book(self):
        """
        Test that a member can find a book
        """
        # John is a member of Waves of Hope Foundation who would like
        # to read Christian books to grow Spiritually. He visits the
        # home page of Waves Resource Center.
        home_page = self.selenium.get(self.live_server_url + '/')

        # He knows he's in the right place because he can see
        # the name of the site in the navbar, as well as a
        # call-to-action message in the heading and lead paragraph.
        brand_element = self.selenium.\
            find_element_by_css_selector('.navbar-brand')
        self.assertEqual('Waves Resource Center', brand_element.text)

        heading1 = self.selenium.find_element_by_tag_name('h1')
        self.assertEqual('Be Empowered Today For Free',
            heading1.text
        )

        lead_paragraph = self.selenium.\
            find_element_by_css_selector('p.lead')
        self.assertEqual('Find books, videos and opportunities '
                + 'that will change your life forever',
            lead_paragraph.text
        )

        # He sees two call-to-action buttons, which are links for
        #  the register and login pages.
        cta_buttons = self.selenium.\
            find_elements_by_css_selector('.homepage-cta .btn')
        self.assertEqual(len(cta_buttons), 2)

        register_link, login_link = cta_buttons
        self.assertEqual('Register', register_link.text)
        self.assertEqual('Login', login_link.text)

        self.fail('Incomplete Test')

        # He doesn't have an account and therefore decides to register. 
        # He clicks on the register link ...

        # ... and is redirected to the register page where he sees
        # a registration form.
        
        # He keys in a username, email, phone number and password and clicks
        # the register button to send the form.

        # The registration was successful, and he is redirected to the
        # login page where he finds a login form.

        # He enters his username and password and clicks the login button
        # to log in to the resource center.

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
