from django.test import TestCase
from django.urls import resolve, reverse


class BookURLsTestCase(TestCase):
    """
    Test URL configuration of books
    """
    def test_book_list_url(self):
        """
        Test that the URL for book list resolves to the
        correct view function
        """
        book_list = resolve(reverse('books'))
        self.assertEqual(book_list.func.__name__, 'BookListView')

    def test_book_details_url(self):
        """
        Test that the URL for book details resolves to the
        correct view function
        """
        book_details = resolve(reverse('book',
            kwargs={'slug': 'the-hydroponics-handbook'}))
        self.assertEqual(book_details.func.__name__,
            'BookDetailView')
