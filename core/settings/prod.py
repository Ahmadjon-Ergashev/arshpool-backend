from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

# logging with redis
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'redis': {
            'level': 'DEBUG',
            'class': 'core.logging.RedisHandler',
            'host': env('REDIS_HOST'),
            'port': env('REDIS_PORT'),
            'key': 'django',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'redis'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Cache with redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}