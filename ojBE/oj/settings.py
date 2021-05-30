"""
Django settings for oj project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import logging
import django.utils.log
import logging.handlers
import os
from pathlib import Path
from os import environ
from datetime import timedelta
from conf.project_conf import (DATABASE_SETTING, HOSTS, EMAIL_SETTING, 
                                REDIS_SETTING, )

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3b*31k%e3-ce1bhc0kl&w^sht0yq4(2y(bof2cir!&tw778_a&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party App
    'rest_framework',
    'django_mysql',
    'corsheaders',
    'channels',
    'celery',
    'django_celery_beat',
    'django_celery_results',
    # 'django_dramatiq',

    # My App
    'account',
    'problem',
    'submission',
    'battle',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'oj.wsgi.application'

ASGI_APPLICATION = "oj.routing.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_SETTING['DATABASE_NAME'],
        'USER': DATABASE_SETTING['DATABASE_USER'],
        'PASSWORD': DATABASE_SETTING['DATABASE_PWD'],
        'HOSR': DATABASE_SETTING['DATABASE_HOST'],
        'PORT': DATABASE_SETTING['DATABASE_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# User Model
AUTH_USER_MODEL = 'account.User'

# Django-REST-Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.AllowAny',
    ),
}

# Auth Backend
AUTHENTICATION_BACKENDS = ('account.backend.LoginBackend', )

# JWT SETTING
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('JWT',),
}

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     '*'
# )

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
    'X-Real-IP',
    'x-Forwarded-For',
    'x-Forwarded-Host',
    'Host',
    'Upgrade',
    'Connection',
    'Sec-WebSocket-Extensions',
    'Sec-WebSocket-Key',
    'Sec-WebSocket-Version',
    'Cache-Control',
)

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_FROM = EMAIL_SETTING['EMAIL_FROM']
EMAIL_HOST = EMAIL_SETTING['EMAIL_HOST']
EMAIL_PORT = EMAIL_SETTING['EMAIL_PORT']
EMAIL_HOST_USER = EMAIL_SETTING['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = EMAIL_SETTING['EMAIL_HOST_PASSWORD']


REDIS_URL = f"redis://{REDIS_SETTING['HOST']}:{REDIS_SETTING['PORT']}"

# Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URL}/{REDIS_SETTING['DB']}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# DRANATIQ
# unused in this project
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "url": f"{REDIS_URL}/4",
    },
    "MIDDLEWARE": [
        # "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        # "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware"
    ]
}

DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKEND_OPTIONS": {
        "url": f"{REDIS_URL}/4",
    },
    "MIDDLEWARE_OPTIONS": {
        "result_ttl": None
    }
}

DRAMATIQ_IGNORED_MODULES = [
    'problem.tasks',
]

# LOGGER
LOGGING_DIR = os.path.join(BASE_DIR, 'log')

LOGGING = {
    'version': 1,
    #  'disable_existing_loggers': True,
     'formatters': {
         'simple': {
             'format': '[%(asctime)s] %(levelname)s : %(message)s'
         },
         'verbose': {
             'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d : %(message)s'
         },
         'standard': {
             'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
         },
     },
     'handlers': {
         'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'run.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
         },
         'error':{
             'level': 'ERROR',
             'class': 'logging.handlers.RotatingFileHandler',
             'filename': os.path.join(LOGGING_DIR, "err.log"),
             'maxBytes': 1024 * 1024 * 100,
             'backupCount': 5,
             'formatter': 'standard',
         },
         'console': {
             'level': 'DEBUG',
             'class': 'logging.StreamHandler',
             'formatter': 'standard',
         },
     },
     'loggers': {
         '': {
             'handlers': ['default', 'error'],
             'level': 'DEBUG',
             'propagate': True,
         },
     },
}

# WebSocket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [f"{REDIS_URL}/{REDIS_SETTING['DB']}", ],
        },
    },
}

# Celery
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = f"{REDIS_URL}/{REDIS_SETTING['DB']}"
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_BEAT_SCHEDULE = {
    'battle_connect': {
        "task": "battle.tasks.battle_connect",
        "schedule": timedelta(seconds=15),
        "args": ()
    }
}