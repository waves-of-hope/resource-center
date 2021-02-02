from .production import *

if os.getenv('GAE_APPLICATION', None):
    # If running on App Engine, connect to Google
    # Cloud SQL using the unix socket
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/' + config('DATABASE_INSTANCE_CONNECTION_NAME'),
            'USER': config('STAGING_DB_USER'),
            'PASSWORD': config('STAGING_DB_PASSWORD'),
            'NAME': config('STAGING_DATABASE'),
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
            'NAME': config('STAGING_DATABASE'),
            'USER': config('STAGING_DB_USER'),
            'PASSWORD': config('STAGING_DB_PASSWORD'),
        }
    }

# Google Cloud Storage bucket settings
GS_BUCKET_NAME = config('STAGING_GCP_STORAGE_BUCKET_NAME')

# Static files
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/static/'

# Media
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/media/'
