from google.oauth2 import service_account

from .base import *

if os.getenv('GAE_APPLICATION', None):
    # If running on App Engine, connect to Google
    # Cloud SQL using the unix socket
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/' + config('DATABASE_INSTANCE_CONNECTION_NAME'),
            'USER': config('PRODUCTION_DB_USER'),
            'PASSWORD': config('PRODUCTION_DB_PASSWORD'),
            'NAME': config('PRODUCTION_DATABASE'),
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
            'NAME': config('PRODUCTION_DATABASE'),
            'USER': config('PRODUCTION_DB_USER'),
            'PASSWORD': config('PRODUCTION_DB_PASSWORD'),
        }
    }

# Google Cloud Storage bucket settings
GS_BUCKET_NAME = config('PRODUCTION_GCP_STORAGE_BUCKET_NAME')
GS_DEFAULT_ACL = 'publicRead'

try:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        config('GOOGLE_CLOUD_STORAGE_SERVICE_ACCOUNT_FILE')
    )
# for environments where storage of files isn't allowed, e.g: Heroku
# TODO: Test if this works
except Exception as e:
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(
        json.loads(config('GOOGLE_CLOUD_STORAGE_SERVICE_ACCOUNT_CREDENTIALS'))
    )

# Static files
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'
STATICFILES_STORAGE = 'utils.storages.StaticRootGoogleCloudStorage'

# Media
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
DEFAULT_FILE_STORAGE = 'utils.storages.MediaRootGoogleCloudStorage'

# Admin URL
ADMIN_URL = config('ADMIN_URL')
