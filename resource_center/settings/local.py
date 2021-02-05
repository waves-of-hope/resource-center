from .base import *

# Django Settings
# ===============

DEBUG = True

ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': config('DATABASE'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
    }
}
