from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Video


class VideoListView(LoginRequiredMixin, ListView):
    """
    Creates the video list page
    """
    model = Video
    template_name = 'core/resource_list.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resources'] = 'videos'
        return context


class VideoDetailView(LoginRequiredMixin, DetailView):
    """
    Creates the video detail pages
    """
    model = Video
    template_name = 'core/video.html'
