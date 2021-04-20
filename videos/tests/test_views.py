from shutil import copy, rmtree

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, tag

from core.models import Category, Tag
from videos.models import Video


class VideoViewsTestCase(TestCase):
    """
    Sets up data to be shared across tests for videos.views
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


class VideoListViewTestCase(VideoViewsTestCase):
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
        self.assertTemplateUsed('core/resource_list.html')

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


class VideoDetailViewTestCase(VideoViewsTestCase):
    """
    Tests for the VideoDetail view
    """
    def test_redirect_if_not_logged_in(self):
        """
        Test that the video detail view redirects to the login page
        first when a user is not logged in
        """
        response = self.client.get('/videos/the-gift/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
            '/accounts/login/?next=/videos/the-gift/')

    def test_video_detail_view_logged_in_basic(self):
        """
        Test that the video detail view returns a 200 response
        and uses the correct template when a user is logged in
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/videos/the-gift/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('core/resource_list.html')
