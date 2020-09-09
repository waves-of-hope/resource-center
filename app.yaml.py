import yaml
from decouple import config

# create configurations for app.yaml
conf = {
    'service': 'waves-resource-center',
    'runtime': 'python38',
    'handlers': [
        {
        'url': '/static',
        'static_dir': 'staticfiles/'
        }, 
        {
        'url': '/.*',
        'script': 'auto'
        }
    ],
    'automatic_scaling': {
        'max_instances': 15,
        'target_cpu_utilization': 0.75,
        # 'target_throughput_utilization': 0.6,
        # 'max_concurrent_requests': 10,
    },
    'env_variables': {
        # Django
        'SECRET_KEY': config('SECRET_KEY'),
        'DEBUG': config('DEBUG', default=False, cast=bool),
        'ALLOWED_HOSTS': config('ALLOWED_HOSTS'),

        # Email
        'EMAIL_HOST_USER': config('EMAIL_HOST_USER'),
        'EMAIL_HOST_PASSWORD': config('EMAIL_HOST_PASSWORD'),
        'ADMINS': config('ADMINS'),
        'MANAGERS': config('MANAGERS'),

        # Cloud Storage
        'GS_BUCKET_NAME': config('GS_BUCKET_NAME'),
        'GS_SA_KEY': config('GS_SA_KEY'),

        # Cloud SQL
        'INSTANCE_CONNECTION_NAME': config('INSTANCE_CONNECTION_NAME'),
        'DATABASE': config('DATABASE'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
    }
}

if __name__ == '__main__':
    with open('app.yaml', 'w') as file:
        yaml.dump(conf, file, sort_keys=False)