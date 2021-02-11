from django.test import TestCase, RequestFactory

from resources import views


class IndexViewTestCase(TestCase):
    """
    Tests for the index view
    """
    def setUp(self):
        self.factory = RequestFactory()

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
