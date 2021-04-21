from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from core.models import Category, Tag
from videos.models import Video


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


class VideoModelTestCase(ResourceModelsTestCase):
    """
    Tests for the Video model
    """
    def test_video_basic(self):
        """
        Test the basic functionality of Video
        """
        self.assertEqual(self.video.title,
            'A Christian\'s guide to wealth creation')
        self.assertIsNotNone(self.video.authors)
        self.assertQuerysetEqual(list(self.video.authors.all()),
            ['<User: Kelvin>', '<User: Alvin>']
        )
        self.assertEqual(self.video.summary,
            'A step-by-step guide on how to handle money'
                'as God has instructed in His Word')
        self.assertEqual(self.video.category.name, 'Finance')
        self.assertQuerysetEqual(list(self.video.tags.all()),
            ['<Tag: Christian finance>', '<Tag: Wealth creation>']
        )
        self.assertEqual(self.video.slug,
            'a-christians-guide-to-wealth-creation')
        self.assertEqual(self.video.url,
            'https://youtu.be/rAKLiE658m0')
        self.assertEqual(self.video.date_posted.date(),
            timezone.now().date())
        self.assertLessEqual(self.video.date_posted, timezone.now())
        self.assertLessEqual(self.video.last_edit, timezone.now())

    def test_video_object_name(self):
        """
        Test the name of the Video object that will
        be shown in django admin
        """
        self.assertEqual(self.video.title, str(self.video))

    def test_title_meta(self):
        """
        Test meta attributes of the title field
        """
        title__meta = self.video._meta.get_field('title')
        self.assertEqual(title__meta.verbose_name, 'title')
        self.assertEqual(title__meta.max_length, 50)
        self.assertEqual(title__meta.null, False)
        self.assertEqual(title__meta.blank, False)

    def test_authors_meta(self):
        """
        Test meta attributes of the authors field
        """
        authors__meta = self.video._meta.get_field('authors')
        self.assertEqual(authors__meta.verbose_name, 'authors')
        self.assertEqual(authors__meta.null, False)
        self.assertEqual(authors__meta.blank, False)

    def test_summary_meta(self):
        """
        Test meta attributes of the summary field
        """
        summary__meta = self.video._meta.get_field('summary')
        self.assertEqual(summary__meta.verbose_name, 'summary')
        self.assertEqual(summary__meta.max_length, 200)
        self.assertEqual(summary__meta.null, True)
        self.assertEqual(summary__meta.blank, True)

    def test_category_meta(self):
        """
        Test meta attributes of the category field
        """
        category__meta = self.video._meta.get_field('category')
        self.assertEqual(category__meta.verbose_name, 'category')
        self.assertEqual(category__meta.null, False)
        self.assertEqual(category__meta.blank, False)

    def test_tags_meta(self):
        """
        Test meta attributes of the tags field
        """
        tags__meta = self.video._meta.get_field('tags')
        self.assertEqual(tags__meta.verbose_name, 'tags')
        self.assertEqual(tags__meta.blank, True)
        self.assertEqual(tags__meta.help_text,
            'Select some tags for this resource'
        )

    def test_slug_meta(self):
        """
        Test meta attributes of the slug field
        """
        slug__meta = self.video._meta.get_field('slug')
        self.assertEqual(slug__meta.verbose_name, 'slug')
        self.assertEqual(slug__meta.help_text,
            'Enter a URL-friendly name')
        self.assertEqual(slug__meta.max_length, 50)
        self.assertEqual(slug__meta.null, False)
        self.assertEqual(slug__meta.blank, False)

    def test_url_meta(self):
        """
        Test meta attributes of the url field
        """
        url__meta = self.video._meta.get_field('url')
        self.assertEqual(url__meta.verbose_name, 'URL')
        self.assertEqual(url__meta.help_text,
            'Enter the video URL here')
        self.assertEqual(url__meta.max_length, 200)
        self.assertEqual(url__meta.null, False)
        self.assertEqual(url__meta.blank, False)

    def test_date_posted_meta(self):
        """
        Test meta attributes of the date posted field
        """
        date_posted__meta = self.video._meta.get_field('date_posted')
        self.assertEqual(date_posted__meta.verbose_name, 'date posted')
        self.assertEqual(date_posted__meta.null, False)
        self.assertEqual(date_posted__meta.blank, False)

    def test_last_edit_meta(self):
        """
        Test meta attributes of the last edit field
        """
        last_edit__meta = self.video._meta.get_field('last_edit')
        self.assertEqual(last_edit__meta.verbose_name, 'last edit')
        self.assertEqual(last_edit__meta.null, False)
        self.assertEqual(last_edit__meta.blank, True)
