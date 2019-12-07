"""
Django settings for beast project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from configparser import RawConfigParser

# Production ready environment variables for Django.
config = RawConfigParser()
config.read('beast/settings.ini')

django_SECRET_KEY = config.get('section', 'django_SECRET_KEY')
postgres_DB_NAME = config.get('section', 'postgres_DB_NAME')
postgres_DB_USER = config.get('section', 'postgres_DB_USER')
postgres_DB_PASSWORD = config.get('section', 'postgres_DB_PASSWORD')
postgres_DB_PUBLIC_IP = config.get('section', 'postgres_DB_PUBLIC_IP')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = django_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = '*'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    # After the default packages
    'graphql_playground',
    'graphene_django',
    # Local apps
    'clips',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Auth Middleware necessary for JWT Auth
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # JWT Authentication Middleware
    'graphql_jwt.middleware.JSONWebTokenMiddleware',
]

ROOT_URLCONF = 'beast.urls'

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

# WSGI_APPLICATION = 'beast.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# PostgreSQL database config:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': postgres_DB_NAME,
#         'USER': postgres_DB_USER,
#         'PASSWORD': postgres_DB_PASSWORD,
#         # https://console.cloud.google.com/sql/instances
#         'HOST': postgres_DB_PUBLIC_IP,
#         # At the moment, Google Cloud PSQL is using the default port 5432
#         'PORT': '5432',
#         # 'OPTIONS': {
#         #     'sslmode': 'verify-ca',  # Leave this line intact
#         #     'sslrootcert': 'beast/beast-app-psql-ssl-certificates/server-ca.pem',
#         #     "sslcert": "beast/beast-app-psql-ssl-certificates/client-cert.pem",
#         #     "sslkey": "beast/beast-app-psql-ssl-certificates/client-key.pem",
#         # }
#     }
# }

# Local SQLite database config:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


# In this simple example we use in-process in-memory Channel layer.
# In a real-life cases you need Redis or something familiar.
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

ASGI_APPLICATION = "beast.routing.application"

GRAPHENE = {
    'SCHEMA': 'beast.schema.schema',
    'SCHEMA_OUTPUT': 'schema.json',  # defaults to schema.json,
    'SCHEMA_INDENT': 2,  # Defaults to None (displays all data on a single line)
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]
