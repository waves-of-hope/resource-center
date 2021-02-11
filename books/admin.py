from django.contrib import admin

from .models import Book
from resources.admin import ResourceAdmin


@admin.register(Book)
class BookAdmin(ResourceAdmin):
    """
    Registers the Book model to the admin site
    """
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'summary')
        }),
        ('External References', {
            'fields': ('authors', 'category', 'tags')
        }),
        ('Uploads', {
            'fields': ('cover_image', 'file_upload'),
        }),
        ('Additional Info', {
            'fields': ('date_posted',)
        })
    )
