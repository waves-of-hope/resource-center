from django.conf import settings
from django.db import models
from django.utils import timezone

class ResourceGroup(models.Model):
    """
    Abstract model for creating Resource Group models
    """
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=30,
        help_text='Enter a URL-friendly name for this resource group')

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(ResourceGroup):
    """
    Model for resource categories
    """

    class Meta(ResourceGroup.Meta):
        verbose_name_plural = 'categories'


class Tag(ResourceGroup):
    """
    Model for resource tags
    """
    description = None


class Resource(models.Model):
    """
    Abstract model for creating Resource models
    """
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_authors",
        related_query_name="%(app_label)s_%(class)s_author"
    )
    summary = models.TextField(max_length=200, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', blank=True,
        help_text='Select some tags for this resource',
        related_name="%(app_label)s_%(class)s_tags",
        related_query_name="%(app_label)s_%(class)s_tag"
        )
    slug = models.SlugField(help_text='Enter a URL-friendly name for this resource')
    date_posted = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def display_tags(self):
        """
        Create a string for the Tags to be displayed in
        the admin site.
        """
        tags = self.tags.all()
        if len(tags) < 3:
            return ', '.join(tag.name for tag in tags)
        return ', '.join(tag.name for tag in tags[:3]) + ' ...'
    
    display_tags.short_description = 'Tags'


class Book(Resource):
    """
    Model for books
    """
    cover_image = models.ImageField(default='book-cover.png',
        upload_to='book_covers',
        help_text='Upload the book\'s cover here'
    )
    file_upload = models.FileField(upload_to='books',
        help_text='Upload the book here')


class Video(Resource):
    """
    Model for videos
    """
    url = models.URLField(help_text='Enter the video URL here')
