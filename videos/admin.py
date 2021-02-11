from django.contrib import admin

from .models import Video
from resources.admin import ResourceAdmin


@admin.register(Video)
class VideoAdmin(ResourceAdmin):
    """
    Registers the Video model to the admin site
    """
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'summary', 'url')
        }),
        ('External References', {
            'fields': ('authors', 'category', 'tags')
        }),
        ('Additional Info', {
            'fields': ('date_posted',)
        })
    )
