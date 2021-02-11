from django.test import TestCase
from django.urls import resolve, reverse


class ResourcesURLsTestCase(TestCase):
    """
    Test URL configuration of resources
    """
    def test_video_list_url(self):
        """
        Test that the URL for video list resolves to the
        correct view function
        """
        video_list = resolve(reverse('videos'))
        self.assertEqual(video_list.func.__name__, 'VideoListView')

    def test_video_details_url(self):
        """
        Test that the URL for video details resolves to the
        correct view function
        """
        video_details = resolve(reverse('video',
            kwargs={'slug': 'the-gift'}))
        self.assertEqual(video_details.func.__name__,
            'VideoDetailView')
