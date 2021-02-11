from django.conf import settings
from django.db import models
from django.utils import timezone


class ResourcesBaseModel(models.Model):
    """
    Defines repetitive fields for both resources and resource groups
    """
    slug = models.SlugField(unique=True,
        help_text='Enter a URL-friendly name')
    last_edit = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ResourceGroup(ResourcesBaseModel):
    """
    Defines repetitive fields for resource groups
    """
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

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


class Resource(ResourcesBaseModel):
    """
    Defines repetitive fields for resources
    """
    title = models.CharField(max_length=50)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s_authors",
        related_query_name="%(app_label)s_%(class)s_author"
    )
    summary = models.TextField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True,
        help_text='Select some tags for this resource',
        related_name="%(app_label)s_%(class)s_tags",
        related_query_name="%(app_label)s_%(class)s_tag"
        )
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def display_tags(self):
        """
        Create a string for the Tags to be displayed in
        the admin site list display.
        """
        tags = self.tags.all()
        if len(tags) < 3:
            return ', '.join(tag.name for tag in tags)
        return ', '.join(tag.name for tag in tags[:3]) + ' ...'

    display_tags.short_description = 'Tags'
