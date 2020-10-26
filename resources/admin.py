from django.contrib import admin

from .models import Category, Tag, Book, Video

class ResourceGroupAdmin(admin.ModelAdmin):
    """
    Defines common admin site configurations for 
    Resource Group models
    """
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(ResourceGroupAdmin):
    """
    Registers the Category model to the admin site
    """
    fields = ('name', 'slug', 'description')


@admin.register(Tag)
class TagAdmin(ResourceGroupAdmin):
    """
    Registers the Tag model to the admin site
    """
    fields = ('name', 'slug')


class ResourceAdmin(admin.ModelAdmin):
    """
    Defines common admin site configurations for
    Resource models
    """    
    list_display = ['title', 'category', 'display_tags']
    prepopulated_fields = {'slug': ('title',)}


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
