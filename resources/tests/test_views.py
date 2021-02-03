from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, override_settings, tag

from resources import views
from resources.models import Category, Tag, Book, Video
from shutil import rmtree, copy


class ResourceViewsTestCase(TestCase):
    """
    Sets up data to be shared across tests for resources.views
    """
    def setUp(self):
        self.factory = RequestFactory()
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT.mkdir()
        copy(
            settings.TEST_FILES_DIR.joinpath('documents/book.pdf'),
            settings.MEDIA_ROOT
        )

        # users
        cls.User = get_user_model()
        cls.kelvin = cls.User.objects.create_superuser(
            first_name = 'Kelvin',
            email='kelvin@murage.com',
            password='kelvinpassword'
        )
        cls.christine = cls.User.objects.create_user(
            first_name = 'Christine',
            last_name = 'Kyalo',
            email = 'christine@kyalo.com',
            phone_number = '+254 723 456 789',
            password = 'christinepassword'
        )

        # categories
        cls.spiritual = Category.objects.create(
            name='Spiritual',
            slug='spiritual'
        )
        cls.agribusiness = Category.objects.create(
            name='Agribusiness',
            slug='agribusiness'
        )

        # tags
        cls.salvation = Tag.objects.create(
            name='Salvation',
            slug='salvation'
        )
        cls.faith = Tag.objects.create(
            name='Faith',
            slug='faith'
        )
        cls.hydroponics = Tag.objects.create(
            name='Hydroponics',
            slug='hydroponics'
        )

        # books
        cls.the_hydroponics_handbook = Book.objects.create(
            title='The Hydroponics handbook',
            summary='A guide to get started in Hydroponics '
                'with little capital',
            category=cls.agribusiness,
            slug='the-hydroponics-handbook',
            cover_image='book-cover.jpg',
            file_upload='book.pdf'
        ) 
        cls.the_hydroponics_handbook.authors.add(cls.kelvin)
        cls.the_hydroponics_handbook.tags.add(cls.hydroponics)

        # Create 8 books for pagination tests
        number_of_books = 8
        for i in range(number_of_books):
            prayer_devotion = Book.objects.create(
                title='Prayer Devotion {}'.format(i),
                category=cls.spiritual,
                slug='prayer-devotion-{}'.format(i),
                cover_image='prayer-devotion-{}.jpg'.format(i),
                file_upload='prayer-devotion-{}.pdf'.format(i)
            ) 
            prayer_devotion.authors.add(cls.kelvin)
        
        # videos
        cls.the_gift = Video.objects.create(
            title='The Gift',
            summary='Explains why and how to recieve God\'s '
                'free gift of salvation',
            category=cls.spiritual,
            slug='the-gift',
            url='https://youtu.be/rAKLiE658m0'
        )
        cls.the_gift.authors.add(cls.kelvin, cls.christine)
        cls.the_gift.tags.add(cls.salvation,
            cls.faith)

        # Create 10 videos for pagination tests
        number_of_videos = 10
        for i in range(number_of_videos):
            the_gift_chapter = Video.objects.create(
                title='The Gift Chapter {}'.format(i),
                category=cls.spiritual,
                slug='the-gift-chapter-{}'.format(i),
                url='https://youtu.be/rAKLiE658m0'
            ) 
            the_gift_chapter.authors.add(cls.kelvin)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # remove test media directory
        rmtree(settings.MEDIA_ROOT)


class IndexViewTestCase(ResourceViewsTestCase):
    """
    Tests for the index view
    """    
    def test_index_view_basic(self):
        """
        Test that index view returns a 200 response and uses
        the correct template
        """
        request = self.factory.get('/')
        with self.assertTemplateUsed('index.html'):
            response = views.index(request)
            self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        """
        Test the index view context
        """
        response = self.client.get('/')
        self.assertEqual(response.context['index'], True)
        self.assertEqual(response.context['num_books'], 9)
        self.assertEqual(response.context['num_videos'], 11)
        self.assertEqual(response.context['num_users'], 2)


class BookListViewTestCase(ResourceViewsTestCase):
    """
    Tests for the BookList view
    """    
    def test_redirect_if_not_logged_in(self):
        """
        Test that the book list view redirects to the login page
        first when a user is not logged in
        """
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
            '/accounts/login/?next=/books/')

    def test_book_list_view_logged_in_basic(self):
        """
        Test that the book list view returns a 200 response
        and uses the correct template when a user is logged in
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('resources/resource_list.html')
    
    @tag('slow')
    def test_books_ordered_by_latest_date_posted(self):
        """
        Test that the  view lists books in descending order
        by date posted
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        latest_date = 0
        for book in response.context['book_list']:
            if latest_date == 0:
                latest_date = book.date_posted
            else:
                self.assertTrue(latest_date >= book.date_posted)
                latest_date = book.date_posted

    def test_book_list_pagination_is_six(self):
        """
        Test that the book list view paginates by 6 books
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['book_list']) == 6)

    def test_view_lists_all_books(self):
        """
        Test that the book list view lists all books when paginated
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/books/'+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['book_list']) == 3)


class VideoListViewTestCase(ResourceViewsTestCase):
    """
    Tests for the VideoList view
    """    
    def test_redirect_if_not_logged_in(self):
        """
        Test that the video list view redirects to the login page
        first when a user is not logged in
        """
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
            '/accounts/login/?next=/videos/')

    def test_video_list_view_logged_in_basic(self):
        """
        Test that the video list view returns a 200 response
        and uses the correct template when a user is logged in
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('resources/resource_list.html')

    @tag('slow')
    def test_videos_ordered_by_latest_date_posted(self):
        """
        Test that the view lists videos in descending order
        by date posted
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, 200)
        latest_date = 0
        for video in response.context['video_list']:
            if latest_date == 0:
                latest_date = video.date_posted
            else:
                self.assertTrue(latest_date >= video.date_posted)
                latest_date = video.date_posted

    def test_video_list_pagination_is_nine(self):
        """
        Test that the video list view paginates by 9 videos
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['video_list']) == 9)

    def test_view_lists_all_videos(self):
        """
        Test that the video list view lists all videos when paginated
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/videos/'+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['video_list']) == 2)
        

class BookDetailViewTestCase(ResourceViewsTestCase):
    """
    Tests for the BookDetail view
    """
    def test_redirect_if_not_logged_in(self):
        """
        Test that the book detail view redirects to the login page
        first when a user is not logged in
        """
        response = self.client.get('/b/the-hydroponics-handbook/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
            '/accounts/login/?next=/b/the-hydroponics-handbook/')

    def test_book_detail_view_logged_in_basic(self):
        """
        Test that the book detail view returns a 200 response
        and uses the correct template when a user is logged in
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/b/the-hydroponics-handbook/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('resources/resource_list.html')


class VideoDetailViewTestCase(ResourceViewsTestCase):
    """
    Tests for the VideoDetail view
    """
    def test_redirect_if_not_logged_in(self):
        """
        Test that the video detail view redirects to the login page
        first when a user is not logged in
        """
        response = self.client.get('/v/the-gift/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
            '/accounts/login/?next=/v/the-gift/')

    def test_video_detail_view_logged_in_basic(self):
        """
        Test that the video detail view returns a 200 response
        and uses the correct template when a user is logged in
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/v/the-gift/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('resources/resource_list.html')
