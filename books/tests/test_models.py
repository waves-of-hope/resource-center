from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from books.models import Book
from resources.models import Category, Tag


class ResourceModelsTestCase(TestCase):
    """
    Sets up data to be shared across Resource Models tests
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = Category.objects.create(
            name='Finance',
            slug='finance'
        )

        cls.tag1 = Tag.objects.create(
            name='Christian finance',
            slug='christian-finance'
        )

        cls.tag2 = Tag.objects.create(
            name='Wealth creation',
            slug='wealth-creation'
        )

        cls.User = get_user_model()

        cls.admin_user = cls.User.objects.create_superuser(
            first_name = 'Kelvin',
            email='kelvin@murage.com',
            password='kelvinpassword'
        )

        cls.user = cls.User.objects.create_user(
            first_name = 'Alvin',
            last_name = 'Mukuna',
            email = 'alvin@mukuna.com',
            phone_number = '+254 701 234 567',
            password = 'alvinpassword'
        )

        cls.book = Book.objects.create(
            title='A Christian\'s guide to wealth creation',
            summary='A step-by-step guide on how to handle money'
                'as God has instructed in His Word',
            category=cls.category,
            slug='a-christians-guide-to-wealth-creation',
            file_upload='book.pdf'
        )
        # Direct assignment of many-to-many types not allowed.
        cls.book.authors.add(cls.admin_user, cls.user)
        cls.book.tags.add(cls.tag1, cls.tag2)


class BookModelTestCase(ResourceModelsTestCase):
    """
    Tests for the Book model
    """
    def test_book_basic(self):
        """
        Test the basic functionality of Book
        """
        self.assertEqual(self.book.title,
            'A Christian\'s guide to wealth creation')
        self.assertIsNotNone(self.book.authors)
        self.assertQuerysetEqual(list(self.book.authors.all()),
            ['<User: Kelvin>', '<User: Alvin>']
        )
        self.assertEqual(self.book.summary,
            'A step-by-step guide on how to handle money'
                'as God has instructed in His Word')
        self.assertEqual(self.book.category.name, 'Finance')
        self.assertQuerysetEqual(list(self.book.tags.all()),
            ['<Tag: Christian finance>', '<Tag: Wealth creation>']
        )
        self.assertEqual(self.book.slug,
            'a-christians-guide-to-wealth-creation')
        self.assertEqual(self.book.cover_image, 'book-cover.png')
        self.assertEqual(self.book.file_upload, 'book.pdf')
        self.assertEqual(self.book.date_posted.date(),
            timezone.now().date())
        self.assertLessEqual(self.book.date_posted, timezone.now())
        self.assertLessEqual(self.book.last_edit, timezone.now())

    def test_book_object_name(self):
        """
        Test the name of the Book object that will
        be shown in django admin
        """
        self.assertEqual(self.book.title, str(self.book))

    def test_title_meta(self):
        """
        Test meta attributes of the title field
        """
        title__meta = self.book._meta.get_field('title')
        self.assertEqual(title__meta.verbose_name, 'title')
        self.assertEqual(title__meta.max_length, 50)
        self.assertEqual(title__meta.null, False)
        self.assertEqual(title__meta.blank, False)

    def test_authors_meta(self):
        """
        Test meta attributes of the authors field
        """
        authors__meta = self.book._meta.get_field('authors')
        self.assertEqual(authors__meta.verbose_name, 'authors')
        self.assertEqual(authors__meta.null, False)
        self.assertEqual(authors__meta.blank, False)

    def test_summary_meta(self):
        """
        Test meta attributes of the summary field
        """
        summary__meta = self.book._meta.get_field('summary')
        self.assertEqual(summary__meta.verbose_name, 'summary')
        self.assertEqual(summary__meta.max_length, 200)
        self.assertEqual(summary__meta.null, True)
        self.assertEqual(summary__meta.blank, True)

    def test_category_meta(self):
        """
        Test meta attributes of the category field
        """
        category__meta = self.book._meta.get_field('category')
        self.assertEqual(category__meta.verbose_name, 'category')
        self.assertEqual(category__meta.null, False)
        self.assertEqual(category__meta.blank, False)

    def test_tags_meta(self):
        """
        Test meta attributes of the tags field
        """
        tags__meta = self.book._meta.get_field('tags')
        self.assertEqual(tags__meta.verbose_name, 'tags')
        self.assertEqual(tags__meta.blank, True)
        self.assertEqual(tags__meta.help_text,
            'Select some tags for this resource'
        )

    def test_slug_meta(self):
        """
        Test meta attributes of the slug field
        """
        slug__meta = self.book._meta.get_field('slug')
        self.assertEqual(slug__meta.verbose_name, 'slug')
        self.assertEqual(slug__meta.help_text,
            'Enter a URL-friendly name')
        self.assertEqual(slug__meta.max_length, 50)
        self.assertEqual(slug__meta.null, False)
        self.assertEqual(slug__meta.blank, False)

    def test_cover_image_meta(self):
        """
        Test meta attributes of the cover image field
        """
        cover_image__meta = self.book._meta.\
            get_field('cover_image')
        self.assertEqual(cover_image__meta.verbose_name, 'cover image')
        self.assertEqual(cover_image__meta.default,
            'book-cover.png')
        self.assertEqual(cover_image__meta.upload_to,
            'book_covers')
        self.assertEqual(cover_image__meta.help_text,
            'Upload the book\'s cover here')
        self.assertEqual(cover_image__meta.null, False)
        self.assertEqual(cover_image__meta.blank, False)

    def test_file_upload_meta(self):
        """
        Test meta attributes of the file upload field
        """
        file_upload__meta = self.book._meta.\
            get_field('file_upload')
        self.assertEqual(file_upload__meta.verbose_name,
            'file upload')
        self.assertEqual(file_upload__meta.upload_to,
            'books')
        self.assertEqual(file_upload__meta.help_text,
            'Upload the book here')
        self.assertEqual(file_upload__meta.null, False)
        self.assertEqual(file_upload__meta.blank, False)

    def test_date_posted_meta(self):
        """
        Test meta attributes of the date posted field
        """
        date_posted__meta = self.book._meta.get_field('date_posted')
        self.assertEqual(date_posted__meta.verbose_name, 'date posted')
        self.assertEqual(date_posted__meta.null, False)
        self.assertEqual(date_posted__meta.blank, False)

    def test_last_edit_meta(self):
        """
        Test meta attributes of the last edit field
        """
        last_edit__meta = self.book._meta.get_field('last_edit')
        self.assertEqual(last_edit__meta.verbose_name, 'last edit')
        self.assertEqual(last_edit__meta.null, False)
        self.assertEqual(last_edit__meta.blank, True)
