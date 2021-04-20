from django.contrib import admin

from core.admin import ResourceAdmin

from .models import Video


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
