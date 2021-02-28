import datetime

from django.utils import timezone

from selenium import webdriver

from .base import ResourceCenterTestCase
from core.models import Category, Tag
from videos.models import Video

class VideosTestCase(ResourceCenterTestCase):
    """Sets up data to be shared across tests for the videos feature

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


class AdminTestCase(VideosTestCase):
    """Test the functionality of the videos feature to superusers
    and users with staff permissions

    Args:
        VideosTestCase (object): A subclass of ResourceCenterTestCase
    """
    def test_that_a_staff_can_manage_videos(self):
        """Tests that a staff can manage videos
        """
        # Kelvin would like to give Christine permissions to login
        # to the admin site and add videos for other viewers to watch.
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

        # He sees links to CORE, Categories, Tags and Videos
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
                find_element_by_link_text('VIDEOS').\
                    get_attribute('href'),
            self.live_server_url + '/admin/videos/'
        )

        self.assertEqual(
            self.browser.\
                find_element_by_link_text('Videos').\
                    get_attribute('href'),
            self.live_server_url + '/admin/videos/video/'
        )

        # Kelvin wants to add a record and a number of videos to Waves
        # Resource Center. He goes back to the homepage of the admin site
        self.browser.find_element_by_css_selector(
            '#site-name a').click()

        self.browser.find_element_by_link_text('Videos').click()

        # He's sees the title, Category and Tags of each video
        # listed with the latest videos first
        video_rows = self.browser.find_elements_by_css_selector('#result_list tr')

        self.assertEqual(video_rows[1].text,
            'The Gift Spiritual Faith, Healing, Love ...')
        self.assertEqual(video_rows[2].text,
            'The Hydroponics handbook Agribusiness Hydroponics')
        self.assertEqual(video_rows[3].text,
            'A Christian\'s guide to wealth creation Spiritual Christian finance')

        # He adds a Video to a Category, Tag and User
        # that already exists
        self.browser.find_element_by_link_text('ADD VIDEO').click()
        video_form = self.browser.find_element_by_id('video_form')

        video_form.find_element_by_name('title').\
            send_keys('Divine Healing')
        video_form.find_element_by_name('authors').\
            find_elements_by_tag_name('option')[3].click()
        video_form.find_element_by_name('summary').\
            send_keys('Outlines how to claim divine healing '
            'that is available to us by faith')
        video_form.find_element_by_name('category').\
            find_elements_by_tag_name('option')[3].click()

        tags_to_choose = [1,2]
        for tag in tags_to_choose:
            video_form.find_element_by_name('tags').\
                find_elements_by_tag_name('option')[tag].click()
        video_form.find_element_by_name('url').\
            send_keys('https://youtu.be/rAKLiE658m0')
        video_form.find_element_by_css_selector(
            '.submit-row input').click()

        video_rows = self.browser.find_elements_by_css_selector(
                '#result_list tr')
        self.assertEqual(
            video_rows[1].text,
            'Divine Healing Spiritual Faith, Healing'
        )

        # He then adds a Video for which the Category, Tags and
        # Author do not yet exist
        self.browser.find_element_by_link_text('ADD VIDEO').click()

        # He adds a Category from the Video page
        video_form = self.browser.find_element_by_id('video_form')
        video_form.find_element_by_id('add_id_category').click()

        self.browser.switch_to.window(self.browser.window_handles[1])
        import time; time.sleep(2)
        category_form = self.browser.find_element_by_id('category_form')
        category_form.find_element_by_name('name').\
            send_keys('Music')
        category_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He adds some Tags from the Video page
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.find_element_by_id('video_form').\
            find_element_by_id('add_id_tags').click()

        self.browser.switch_to.window(self.browser.window_handles[1])
        tag_form = self.browser.find_element_by_id('tag_form')
        tag_form.find_element_by_name('name').\
            send_keys('Praise')
        tag_form.find_element_by_css_selector(
            '.submit-row input').click()

        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.find_element_by_id('video_form').\
            find_element_by_id('add_id_tags').click()

        self.browser.switch_to.window(self.browser.window_handles[1])
        tag_form = self.browser.find_element_by_id('tag_form')
        tag_form.find_element_by_name('name').\
            send_keys('Worship')
        tag_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He adds an Author from the Video page
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.find_element_by_id('video_form').\
            find_element_by_id('add_id_authors').click()

        self.browser.switch_to.window(self.browser.window_handles[1])
        user_form = self.browser.find_element_by_id('user_form')
        user_form.find_element_by_css_selector(
            'input#id_first_name').send_keys('Peter')
        user_form.find_element_by_css_selector(
            'input#id_last_name').send_keys('Macharia')
        user_form.find_element_by_css_selector(
            'input#id_email').send_keys('peter@macharia.com')
        user_form.find_element_by_css_selector(
            'input#id_phone_number').send_keys('+254 767 890 123')
        user_form.find_element_by_css_selector(
            'input#id_password1').send_keys('peterpassword')
        user_form.find_element_by_css_selector(
            'input#id_password2').send_keys('peterpassword')
        user_form.find_element_by_css_selector(
            '.submit-row input').click()

        # He adds the Video's details and saves it
        self.browser.switch_to.window(self.browser.window_handles[0])
        video_form = self.browser.find_element_by_id('video_form')
        video_form.find_element_by_name('title').\
            send_keys('Mastering African Praise and Worship Music')
        video_form.find_element_by_name('url').\
            send_keys('https://youtu.be/rAKLiE658m0')
        video_form.find_element_by_css_selector(
            '.submit-row input').click()

        video_rows = self.browser.find_elements_by_css_selector(
            '#result_list tr')
        self.assertEqual(
            video_rows[1].text,
            'Mastering African Praise and Worship Music '
            'Music Praise, Worship'
        )


class MemberTestCase(VideosTestCase):
    """Tests the functionality of the videos feature to members
    and unregistered users

    Args:
        VideosTestCase (object): A subclass of ResourceCenterTestCase
    """
    def test_that_a_user_can_watch_videos(self):
        """Tests that a user can see the video list page and watch videos
        in the detail pages
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
        self.assertEqual(
            register_form.find_element_by_css_selector(
                'label[for="id_first_name"]').text,
            'First name*'
        )

        last_name_input = register_form.\
            find_element_by_css_selector('input#id_last_name')
        self.assertEqual(
            register_form.find_element_by_css_selector(
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

        # The login was successful and he is redirected to the books
        # list page, where he finds some books.
        self.assertEqual(
            self.browser.current_url,
            '{}/books/'.format(self.live_server_url)
        )

        # He finds a videos link in the navbar, clicks it and
        # is redirected to the videos list page, where he finds
        # some videos.
        navbar = self.browser.\
            find_element_by_css_selector('.navbar')
        videos_link = navbar.find_element_by_link_text('Videos')
        self.assertEqual(
            videos_link.get_attribute('href'),
            '{}/videos/'.format(self.live_server_url)
        )

        videos_link.click()
        self.assertEqual(
            self.browser.current_url,
            '{}/videos/'.format(self.live_server_url)
        )

        videos = self.browser.\
            find_elements_by_css_selector('.video-card')
        self.assertGreater(len(videos), 0)

        # The videos list page is paginated
        # TODO: reduce complexity
        pagination = self.browser.find_element_by_css_selector('nav ul.pagination')
        page_links, page_link_addresses = list(), list()
        for i in range(7):
            if i == 0:
                page_links.append('Previous')
                page_link_addresses.append('/videos/#')
            elif i == 7:
                page_links.append('Next')
            else:
                page_link_addresses.append('/videos/?page={}/'.\
                    format(i))

        for i, link in enumerate(page_links):
            self.assertEqual(pagination.find_element_by_link_text(
                    page_links[i]).get_attribute('href'),
                self.live_server_url + page_link_addresses[i]
            )

        # He clicks on the first video and is taken to the video's
        # detail page where he can watch it.
        videos[0].find_element_by_css_selector(
            '.card-title a').click()
        self.assertEqual(
            self.browser.current_url,
            '{}/videos/the-gift/'.format(self.live_server_url)
        )

        self.assertEqual(
            self.browser.find_element_by_css_selector(
                '.card-title').text,
            'The Gift'
        )

        m2m_attributes = self.browser.find_elements_by_css_selector('.m2m-attribute')
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

        youtube_iframe = self.browser.\
            find_element_by_tag_name('iframe')
        self.assertEqual(youtube_iframe.get_attribute('src'),
            'http://www.youtube.com/embed/rAKLiE658m0?wmode=opaque'
        )
