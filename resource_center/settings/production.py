import os

from .base import *

# Django Settings
# ===============

# Email
ADMINS = eval(config('ADMINS'))

MANAGERS = ADMINS


# Cloud SQL Database with App Engine
# https://cloud.google.com/python/django/appengine#understanding_the_code

if os.getenv('GAE_APPLICATION', None):
    # If running on App Engine, connect to Google
    # Cloud SQL using the unix socket
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/' + config('DATABASE_INSTANCE_CONNECTION_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'NAME': config('DATABASE'),
        }
    }

else:
    # Alternatively, connect to either a local MySQL instance
    #  or connect to Cloud SQL via the proxy.
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




# Third Party Apps Settings
# =========================

# Django Storages: Google Cloud Storage
# https://django-storages.readthedocs.io/en/latest/backends/gcloud.html#settings

GS_BUCKET_NAME = config('GCP_STORAGE_BUCKET_NAME')

## Commented out this because it causes the following error:
## "Anonymous caller does not have storage.objects.get access
##  to the Google Cloud Storage object" when trying to access
## files uploaded by another entity (user/ service account)
# GS_DEFAULT_ACL = 'publicRead'

## The default authentication method is getting credentials from
## the env var GOOGLE_APPLICATION_CREDENTIALS
## For environments where storage of files isn't allowed, e.g: Heroku
## TODO: Test if this works
# try:
#     import json
#     from google.oauth2 import service_account

#     GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
#         json.loads(config('GOOGLE_CLOUD_STORAGE_SERVICE_ACCOUNT_CREDENTIALS'))
#     )
# except Exception as e:
#     print(e)


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

ADMIN_URL = config('admin_URL')
