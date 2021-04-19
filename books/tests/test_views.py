from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, tag

from books.models import Book
from core.models import Category, Tag
import utils.test


class BookViewsTestCase(TestCase):
    """
    Sets up data to be shared across tests for books.views
    """
    def setUp(self):
        self.factory = RequestFactory()
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        utils.test.set_up_test_files()

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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        utils.test.tear_down_test_files()


class BookListViewTestCase(BookViewsTestCase):
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
        self.assertTemplateUsed('core/resource_list.html')
    
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


class BookDetailViewTestCase(BookViewsTestCase):
    """
    Tests for the BookDetail view
    """
    def test_redirect_if_not_logged_in(self):
        """
        Test that the book detail view redirects to the login page
        first when a user is not logged in
        """
        response = self.client.get('/books/the-hydroponics-handbook/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
            '/accounts/login/?next=/books/the-hydroponics-handbook/')

    def test_book_detail_view_logged_in_basic(self):
        """
        Test that the book detail view returns a 200 response
        and uses the correct template when a user is logged in
        """
        self.client.login(email = 'christine@kyalo.com',
            password = 'christinepassword'
        )
        response = self.client.get('/books/the-hydroponics-handbook/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('core/resource_list.html')
