"""
Django settings for atalaku project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from pathlib import Path
from django.utils.translation import ugettext_lazy as _
import django.dispatch

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['ATALAKU_SECRET_KEY']
PAY_REQUEST_URL = os.getenv('ATALAKU_PAY_REQUEST_URL')
PAY_USERNAME = os.getenv('ATALAKU_PAY_REQUEST_USERNAME')
PAY_REQUEST_TOKEN = os.getenv('ATALAKU_PAY_REQUEST_TOKEN')
REQUESTER_NAME = os.getenv('ATALAKU_PAY_REQUESTER_NAME', 'ATALAKU')

CELERY_BROKER_URL   = os.environ.get('ATALAKU_CELERY_BROKER_URL')
CELERY_BACKEND      = os.environ.get('ATALAKU_CELERY_BACKEND')

CREDENTIALS_FILE = os.environ.get('ATALAKU_CREDENTIALS_FILE', "credentials.json")

CELERY_DEFAULT_QUEUE = "atalaku-default"
CELERY_DEFAULT_EXCHANGE = "atalaku-default"
CELERY_DEFAULT_ROUTING_KEY = "atalaku-default"

CELERY_LOGGER_HANDLER_NAME = "async"
CELERY_LOGGER_NAME = "async"
CELERY_LOGGER_QUEUE = "atalaku-logger"
CELERY_LOGGER_EXCHANGE = "atalaku-logger"
CELERY_LOGGER_ROUTING_KEY = "atalaku-logger"

CELERY_OUTGOING_MAIL_QUEUE = "atalaku-outgoing-mails"
CELERY_OUTGOING_MAIL_EXCHANGE = "atalaku-mail"
CELERY_OUTGOING_MAIL_ROUTING_KEY = "atalaku.mail.outgoing"


CELERY_IDENTIFICATION_QUEUE = "atalaku-ident"
CELERY_IDENTIFICATION_EXCHANGE = "atalaku-ident"
CELERY_IDENTIFICATION_ROUTING_KEY = "atalaku.identification"
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'

CELERY_NAMESPACE = 'CELERY'
CELERY_APP_NAME = 'atalaku'


DEFAULT_LOCAL_CURRENCY = os.getenv('ATALAKU_CURRENCY')
# SECURITY WARNING: don't run with debug turned on in production!


PAGINATED_BY = 10
ALLOWED_HOSTS = [os.getenv('ATALAKU_ALLOWED_HOST')]
SITE_HEADER_BG = "#eadbcb"
SITE_HOST = os.getenv('ATALAKU_HOST')
SITE_NAME = os.environ['ATALAKU_SITE_NAME']
META_KEYWORDS = "Event,Events, Africa, Africans, Africains, Evènement, Publicité, publication, party, fête,anniversaire"
META_DESCRIPTION = "ATALAKU est un site de publication des evenements africains qui on lieu n'importe où dans le monde"
# Application definition
EMAIL_HOST = os.environ.get('ATALAKU_EMAIL_HOST')
EMAIL_PORT = os.environ.get('ATALAKU_EMAIL_PORT')
EMAIL_HOST_PASSWORD = os.environ.get('ATALAKU_EMAIL_PASSWORD')
EMAIL_HOST_USER = os.environ.get('ATALAKU_EMAIL_USER')
DEFAULT_FROM_EMAIL = os.environ.get('ATALAKU_DEFAULT_FROM_EMAIL', 'ATALAKU <info@atalaku.com>')
CONTACT_MAIL =  os.environ.get('ATALAKU_CONTACT_MAIL')
ADMIN_EXTERNAL_EMAIL = os.environ.get("ATALAKU_ADMIN_EXTERNAL_EMAIL")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_BACKEND = os.environ.get('ATALAKU_EMAIL_BACKEND')
DJANGO_EMAIL_TEMPLATE = "tags/template_email_new.html"
DJANGO_EMAIL_TO_ADMIN_TEMPLATE = "tags/admin_newuser_template_email.html"
DJANGO_EMAIL_TEMPLATE_TXT = "tags/template_email.txt"
DJANGO_WELCOME_EMAIL_TEMPLATE = "welcome_email_new.html"
DJANGO_VALIDATION_EMAIL_TEMPLATE = "validation_email_new.html"
DJANGO_PUBLISHED_CONFIRMATION_EMAIL_TEMPLATE = "tags/published_confirmation_email_new.html"
SEND_USER_LOGGED_IN_SIGNAL = True
SEND_USER_REGISTERED_SIGNAL = True
SIGNA_USER_LOGGED_IN = django.dispatch.Signal()
SIGNA_USER_REGISTERED = django.dispatch.Signal()

TEST_USER_PREFIX = "testuser_"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',
    'core.apps.CoreConfig',
    'events.apps.EventsConfig',
    'dashboard.apps.DashboardConfig',
    'rest_framework',
    'rest_framework.authtoken',
]

# RESTFRAMEWORK SETTINGS
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'atalaku.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.core_context',
                'atalaku.context_processors.site_context',
                'events.context_processors.event_context',
            ],
        },
    },
]


WSGI_APPLICATION = 'atalaku.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'dev': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, f"{SITE_NAME}.db"),
    },
    'production': {
	'ENGINE':   os.environ['ATALAKU_DATABASE_ENGINE'],
	'NAME'	:   os.environ['ATALAKU_DATABASE_NAME'],
	'USER'	:   os.environ['ATALAKU_DATABASE_USERNAME'],
	'PASSWORD': os.environ['ATALAKU_DATABASE_PW'],
	'HOST'	:   os.environ['ATALAKU_DATABASE_HOST'] ,
	'PORT' 	:   os.environ['ATALAKU_DATABASE_PORT'],
    'OPTIONS' : {
        'sslmode': 'require'
    },
    'TEST'  :   {
        'NAME': os.getenv('ATALAKU_TEST_DATABASE', 'test_atalakdb'),
    },
   },

}

DEFAULT_DATABASE = os.environ.get('DJANGO_DATABASE', 'dev')
DATABASES['default'] = DATABASES[DEFAULT_DATABASE]
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get(f"{SITE_NAME}_DEBUG",'false') == 'true'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

###############

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'file': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'async': {
            'format': '{message}',
            'style': '{',
        },
    },

    'handlers': {
        'async':{
            'level': 'INFO',
            'class': 'core.logging.handlers.AsyncLoggingHandler',
            'formatter': 'async',
            'queue': CELERY_LOGGER_QUEUE,
            'routing_key': CELERY_LOGGER_ROUTING_KEY,
            'exchange': CELERY_LOGGER_EXCHANGE
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },

        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename':'logs/atalaku.log',
            'when' : 'midnight'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '' : {
            'level': 'WARNING',
            'handlers': ['console', 'async']
        },
        'async':{
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False
        },
        'django': {
            'level': 'WARNING',
            'handlers': ['async'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'async'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console', 'async'],
            'level': 'WARNING',
            'propagate': True,
        },
        'PIL':{
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en',_('English')),
    ('fr',_('French')),
)
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "staticfiles"),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'