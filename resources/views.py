from django.contrib.auth import get_user_model
from django.shortcuts import render


def index(request):
    """
    Creates the homepage of the site
    """
    context = {'index': True}
    context['num_books'] = 78
    context['num_videos'] = 67
    context['num_users'] = 56
    return render(request, 'index.html', context)
