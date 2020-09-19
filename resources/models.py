from django.conf import settings
from django.db import models
from django.utils import timezone

class Book(models.Model):
    """
    Stores book instances in the database
    """
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    summary = models.TextField(max_length=200, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField('Tag', blank=True,
        help_text='Select some tags for this book')
    slug = models.SlugField()
    cover_image = models.ImageField('Upload the book\'s cover here',
        default='book-cover.png',
        upload_to='book_covers'
    )
    file_upload = models.FileField('Upload the book here',
        upload_to='books')
    date_posted = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    class Meta:
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

class Category(models.Model):
    """
    Stores resource categories in the database
    """
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=30)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Tag(models.Model):
    """
    Stores resource tags in the database
    """
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=30)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name