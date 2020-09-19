from django.contrib import admin

from .models import Category, Tag, Book

admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'display_tags']
