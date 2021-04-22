import os

from utils.config import list_of_tuples

from .base import *

# Django Settings
# ===============

# Email
ADMINS =  decouple.config('ADMINS', cast=list_of_tuples)

MANAGERS = ADMINS

if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection string>
    DATABASES = {
        'default': {
            'ENGINE':  decouple.config('DB_ENGINE', default='django.db.backends.mysql'),
            'HOST': '/cloudsql/' +  decouple.config('DATABASE_INSTANCE_CONNECTION_NAME'),
            'USER':  decouple.config('DB_USER'),
            'PASSWORD':  decouple.config('DB_PASSWORD'),
            'NAME':  decouple.config('DB_NAME'),
        }
    }



# Third Party Apps Settings
# =========================

# Django Storages: Google Cloud Storage
# https://django-storages.readthedocs.io/en/latest/backends/gcloud.html#settings

GS_BUCKET_NAME =  decouple.config('GCP_STORAGE_BUCKET_NAME')

## Commented out this because it causes the following error:
## "Anonymous caller does not have storage.objects.get access
##  to the Google Cloud Storage object" when trying to access
## files uploaded by another entity (user/ service account)
# GS_DEFAULT_ACL = 'publicRead'


# Django Settings that depend on 3rd party app settings
# ------------------------------------------------------

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/ref/settings/#static-files

STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'

STATICFILES_STORAGE = 'utils.storages.StaticRootGoogleCloudStorage'


# Media (user uploaded files)
# https://docs.djangoproject.com/en/3.1/ref/settings/#file-uploads

MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'

DEFAULT_FILE_STORAGE = 'utils.storages.MediaRootGoogleCloudStorage'



# Project Specific Settings
# =========================

ADMIN_URL =  decouple.config('ADMIN_URL')
