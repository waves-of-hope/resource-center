from django.db import models
from django.urls import reverse

from core.models import Resource


class Book(Resource):
    """
    Model for books
    """
    cover_image = models.ImageField(default='book-cover.png',
        upload_to='book_covers',
        help_text="Upload the book's cover here"
    )
    file_upload = models.FileField(upload_to='books',
        help_text='Upload the book here')

    def get_absolute_url(self):
        return reverse('book', kwargs={'slug': self.slug})
