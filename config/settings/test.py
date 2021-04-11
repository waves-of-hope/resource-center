from .base import *

# Django Settings
# ===============

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_HOST = 'localhost'

EMAIL_PORT = 25

MEDIA_ROOT = BASE_DIR / 'test_media'
