from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, override_settings

from resource_center.settings import BASE_DIR
from resources import views
from resources.models import Category, Tag, Book, Video
from shutil import rmtree, copy

@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
@override_settings(MEDIA_ROOT=BASE_DIR / 'test_media')
class ResourceViewsTestCase(TestCase):
    """
    Sets up data to be shared across tests for resources.views
    """
    def setUp(self):
        self.factory = RequestFactory()
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.TEST_FILES_DIR = BASE_DIR / 'test_files'
        cls.MEDIA_ROOT = BASE_DIR / 'test_media'
        cls.MEDIA_ROOT.mkdir()
        copy(cls.TEST_FILES_DIR.joinpath('documents/book.pdf'),
            cls.MEDIA_ROOT)

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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # remove test media directory
        rmtree(cls.MEDIA_ROOT)


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
        self.assertEqual(response.context['num_books'], 1)
        self.assertEqual(response.context['num_videos'], 1)
        self.assertEqual(response.context['num_users'], 2)


class BookListViewTestCase(ResourceViewsTestCase):
    """
    Tests for the BookList view
    """
    def test_book_list_view_basic(self):
        """
        Test that the book list view returns a 200 response
        and uses the correct template
        """
        request = self.factory.get('/books/')
        response = views.BookListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('resources/resource_list.html'):
            response.render()


class VideoListViewTestCase(ResourceViewsTestCase):
    """
    Tests for the VideoList view
    """
    def test_video_list_view_basic(self):
        """
        Test that the video list view returns a 200 response
        and uses the correct template
        """
        request = self.factory.get('/videos/')
        response = views.VideoListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('resources/resource_list.html'):
            response.render()
        

class BookDetailViewTestCase(ResourceViewsTestCase):
    """
    Tests for the BookDetail view
    """
    def test_book_detail_view_basic(self):
        """
        Test that the book list view returns a 200 response
        and uses the correct template
        """
        request = self.factory.get('/b/the-hydroponics-handbook/')
        response = views.BookDetailView.as_view()(
            request,
            slug=self.the_hydroponics_handbook.slug
        )
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('resources/book.html'):
            response.render()


class VideoDetailViewTestCase(ResourceViewsTestCase):
    """
    Tests for the VideoList view
    """
    def test_video_detail_view_basic(self):
        """
        Test that the video list view returns a 200 response
        and uses the correct template
        """
        request = self.factory.get('/v/the-gift/')
        response = views.VideoDetailView.as_view()(
            request,
            slug=self.the_gift.slug         
        )
        self.assertEqual(response.status_code, 200)
        with self.assertTemplateUsed('resources/video.html'):
            response.render()
