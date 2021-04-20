from django.contrib import admin

from core.admin import ResourceAdmin

from .models import Book


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
