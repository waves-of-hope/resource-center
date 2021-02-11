from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from resources.models import Category, Tag

class CategoryModelTestCase(TestCase):
    """
    Tests for the Category model
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = Category.objects.create(
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
        self.assertEqual(self.category.slug, 'spiritual')
        self.assertLessEqual(self.category.date_created, timezone.now())
        self.assertLessEqual(self.category.last_edit, timezone.now())

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
        self.assertEqual(slug__meta.help_text,
            'Enter a URL-friendly name')
        self.assertEqual(slug__meta.max_length, 50)
        self.assertEqual(slug__meta.null, False)
        self.assertEqual(slug__meta.blank, False)

    def test_date_created_meta(self):
        """
        Test meta attributes of the date created field
        """
        date_created__meta = self.category._meta.get_field('date_created')
        self.assertEqual(date_created__meta.verbose_name, 'date created')
        self.assertEqual(date_created__meta.null, False)
        self.assertEqual(date_created__meta.blank, True)

    def test_last_edit_meta(self):
        """
        Test meta attributes of the last edit field
        """
        last_edit__meta = self.category._meta.get_field('last_edit')
        self.assertEqual(last_edit__meta.verbose_name, 'last edit')
        self.assertEqual(last_edit__meta.null, False)
        self.assertEqual(last_edit__meta.blank, True)


class TagModelTestCase(TestCase):
    """
    Tests for the Tag model
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.tag = Tag.objects.create(
            name='Salvation',
            slug='salvation'
        )

    def test_tag_basic(self):
        """
        Test the basic functionality of Tag
        """
        self.assertEqual(self.tag.name, 'Salvation')
        self.assertEqual(self.tag.slug, 'salvation')
        self.assertLessEqual(self.tag.date_created, timezone.now())
        self.assertLessEqual(self.tag.last_edit, timezone.now())

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

    def test_slug_meta(self):
        """
        Test meta attributes of the slug field
        """
        slug__meta = self.tag._meta.get_field('slug')
        self.assertEqual(slug__meta.verbose_name, 'slug')
        self.assertEqual(slug__meta.help_text,
            'Enter a URL-friendly name')
        self.assertEqual(slug__meta.max_length, 50)
        self.assertEqual(slug__meta.null, False)
        self.assertEqual(slug__meta.blank, False)

    def test_date_created_meta(self):
        """
        Test meta attributes of the date created field
        """
        date_created__meta = self.tag._meta.get_field('date_created')
        self.assertEqual(date_created__meta.verbose_name, 'date created')
        self.assertEqual(date_created__meta.null, False)
        self.assertEqual(date_created__meta.blank, True)

    def test_last_edit_meta(self):
        """
        Test meta attributes of the last edit field
        """
        last_edit__meta = self.tag._meta.get_field('last_edit')
        self.assertEqual(last_edit__meta.verbose_name, 'last edit')
        self.assertEqual(last_edit__meta.null, False)
        self.assertEqual(last_edit__meta.blank, True)


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

        cls.video = Video.objects.create(
            title='A Christian\'s guide to wealth creation',
            summary='A step-by-step guide on how to handle money'
                'as God has instructed in His Word',
            category=cls.category,
            slug='a-christians-guide-to-wealth-creation',
            url='https://youtu.be/rAKLiE658m0'
        )
        cls.video.authors.add(cls.admin_user, cls.user)
        cls.video.tags.add(cls.tag1, cls.tag2)
