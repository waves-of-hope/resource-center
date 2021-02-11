from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Book


class BookListView(LoginRequiredMixin, ListView):
    """
    Creates the book list page
    """
    model = Book
    template_name = 'resources/resource_list.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resources'] = 'books'
        return context


class BookDetailView(LoginRequiredMixin, DetailView):
    """
    Creates the book detail pages
    """
    model = Book
    template_name = 'resources/book.html'
