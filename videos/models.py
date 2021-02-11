from django.db import models
from django.urls import reverse

from resources.models import Resource


class Video(Resource):
    """
    Model for videos
    """
    url = models.URLField('URL', help_text='Enter the video URL here')

    def get_absolute_url(self):
        return reverse('video', kwargs={'slug': self.slug})
