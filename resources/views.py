from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Book, Video

def index(request):
    """
    Creates the homepage of the site
    """
    context = {'index': True}
    context['num_books'] = Book.objects.count()
    context['num_videos'] = Video.objects.count()
    context['num_users'] = get_user_model().objects.count()
    return render(request, 'index.html', context)


class BookListView(LoginRequiredMixin, ListView):
    """
    Creates the book list page
    """
    model = Book
    template_name = 'resources/resource_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resources'] = 'books'
        return context


class VideoListView(LoginRequiredMixin, ListView):
    """
    Creates the video list page
    """
    model = Video
    template_name = 'resources/resource_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resources'] = 'videos'
        return context


class BookDetailView(LoginRequiredMixin, DetailView):
    """
    Creates the book detail pages
    """
    model = Book
    template_name = 'resources/book.html'


class VideoDetailView(LoginRequiredMixin, DetailView):
    """
    Creates the video detail pages
    """
    model = Video
    template_name = 'resources/video.html'
