from django.test import TestCase
from django.urls import resolve

from resources.views import index

class ResourcesURLsTestCase(TestCase):
    """
    Test URL configuration of resources
    """
    def test_root_url_uses_index_view(self):
        """
        Test that the root of the site resolves to the
        correct view function
        """
        root = resolve('/')
        self.assertEqual(root.func, index)
