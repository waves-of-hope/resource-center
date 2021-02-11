from django.contrib import admin

from .models import Category, Tag


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
