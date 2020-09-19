from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from resources.models import Category, Tag, Book

class BookModelTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Finance',
            slug='finance'
        )

        self.tag1 = Tag.objects.create(
            name='Christian finance',
            description='Explores the topic of finance from '
                'a Christian perspective',
            slug='christian-finance'
        )

        self.tag2 = Tag.objects.create(
            name='Wealth creation',
            slug='wealth-creation'
        )

        self.User = get_user_model()
        
        self.admin_user = self.User.objects.create_superuser(
            first_name = 'Kelvin',
            email='kelvin@murage.com',
            password='kelvinpassword'
        )

        self.user = self.User.objects.create_user(
            first_name = 'Alvin',
            last_name = 'Mukuna',
            email = 'alvin@mukuna.com',
            phone_number = '+254 701 234 567',
            password = 'alvinpassword'
        )
            
        self.book = Book.objects.create(
            title='A Christian\'s guide to wealth creation',
            summary='A step-by-step guide on how to handle money'
                'as God has instructed in His Word',
            category=self.category,
            slug='a-christians-guide-to-wealth-creation'
        )        
        # Direct assignment of many-to-many types not allowed.
        self.book.authors.add(self.admin_user, self.user)
        self.book.tags.add(self.tag1, self.tag2)

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
        self.assertEqual(self.book.date_posted.date(),
            timezone.now().date())
        self.assertEqual(self.book.date_posted.strftime('%H:%M:%S'),
            timezone.now().strftime('%H:%M:%S'))
        self.assertEqual(self.book.last_edit, None)

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
            'Select some tags for this book'
        )

    def test_slug_meta(self):
        """
        Test meta attributes of the slug field
        """
        slug__meta = self.book._meta.get_field('slug')
        self.assertEqual(slug__meta.verbose_name, 'slug')
        self.assertEqual(slug__meta.max_length, 50)
        self.assertEqual(slug__meta.null, False)
        self.assertEqual(slug__meta.blank, False)

    def test_cover_image_meta(self):
        """
        Test meta attributes of the cover image field
        """
        cover_image__meta = self.book._meta.\
            get_field('cover_image')
        self.assertEqual(cover_image__meta.verbose_name,
            'Upload the book\'s cover here'
        )
        self.assertEqual(cover_image__meta.default,
            'book-cover.png'
        )
        self.assertEqual(cover_image__meta.upload_to,
            'book_covers'
        )
        self.assertEqual(cover_image__meta.null, False)
        self.assertEqual(cover_image__meta.blank, False)

    def test_file_upload_meta(self):
        """
        Test meta attributes of the file upload field
        """
        file_upload__meta = self.book._meta.\
            get_field('file_upload')
        self.assertEqual(file_upload__meta.verbose_name,
            'Upload the book here'
        )
        self.assertEqual(file_upload__meta.upload_to,
            'books'
        )
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
        self.assertEqual(last_edit__meta.null, True)
        self.assertEqual(last_edit__meta.blank, True)


class CategoryModelTestCase(TestCase):

    def setUp(self):        
        self.category = Category.objects.create(
            name='Spiritual',
            description='Materials that can help you grow '
                'Spiritually',
            slug='spiritual'
        )

    def test_category_basic(self):
        """
        Test the basic functionality of Category
        """
        self.assertEqual(self.category.name, 'Spiritual')
        self.assertEqual(self.category.description,
            'Materials that can help you grow Spiritually')

    def test_category_object_name(self):
        """
        Test the name of the Category object that will
        be shown in django admin
        """
        self.assertEqual(self.category.name, str(self.category))

    def test_name_meta(self):
        """
        Test meta attributes of the name field
        """
        name__meta = self.category._meta.get_field('name')
        self.assertEqual(name__meta.verbose_name, 'name')
        self.assertEqual(name__meta.max_length, 30)
        self.assertEqual(name__meta.null, False)
        self.assertEqual(name__meta.blank, False)

    def test_description_meta(self):
        """
        Test meta attributes of the description field
        """
        description__meta = self.category._meta.get_field('description')
        self.assertEqual(description__meta.verbose_name, 'description')
        self.assertEqual(description__meta.max_length, 100)
        self.assertEqual(description__meta.null, True)
        self.assertEqual(description__meta.blank, True)

    def test_slug_meta(self):
        """
        Test meta attributes of the slug field
        """
        slug__meta = self.category._meta.get_field('slug')
        self.assertEqual(slug__meta.verbose_name, 'slug')
        self.assertEqual(slug__meta.max_length, 30)
        self.assertEqual(slug__meta.null, False)
        self.assertEqual(slug__meta.blank, False)


class TagModelTestCase(TestCase):

    def setUp(self):        
        self.tag = Tag.objects.create(
            name='Getting born again',
            description='Addresses why and how to accept God\'s '
                'free gift of salvation',
            slug='getting-born-again'
        )

    def test_tag_basic(self):
        """
        Test the basic functionality of Tag
        """
        self.assertEqual(self.tag.name, 'Getting born again')
        self.assertEqual(self.tag.description,
            'Addresses why and how to accept God\'s '
                'free gift of salvation')
        
    def test_tag_object_name(self):
        """
        Test the name of the Tag object that will
        be shown in django admin
        """
        self.assertEqual(self.tag.name, str(self.tag))

    def test_name_meta(self):
        """
        Test meta attributes of the name field
        """
        name__meta = self.tag._meta.get_field('name')
        self.assertEqual(name__meta.verbose_name, 'name')
        self.assertEqual(name__meta.max_length, 30)
        self.assertEqual(name__meta.null, False)
        self.assertEqual(name__meta.blank, False)

    def test_description_meta(self):
        """
        Test meta attributes of the description field
        """
        description__meta = self.tag._meta.get_field('description')
        self.assertEqual(description__meta.verbose_name, 'description')
        self.assertEqual(description__meta.max_length, 100)
        self.assertEqual(description__meta.null, True)
        self.assertEqual(description__meta.blank, True)

    def test_slug_meta(self):
        """
        Test meta attributes of the slug field
        """
        slug__meta = self.tag._meta.get_field('slug')
        self.assertEqual(slug__meta.verbose_name, 'slug')
        self.assertEqual(slug__meta.max_length, 30)
        self.assertEqual(slug__meta.null, False)
        self.assertEqual(slug__meta.blank, False)
