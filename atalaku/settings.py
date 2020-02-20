"""
Django settings for atalaku project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['ATALAKU_SECRET_KEY']
PAY_REQUEST_URL = os.getenv('ATALAKU_PAY_REQUEST_URL')
PAY_USERNAME = os.getenv('ATALAKU_PAY_REQUEST_USERNAME')
PAY_REQUEST_TOKEN = os.getenv('ATALAKU_PAY_REQUEST_TOKEN')
REQUESTER_NAME = 'ATALAKU'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','http://atalaku.com', 'www.atalaku.com','atalaku.com', os.environ['ATALAKU_ALLOWED_HOST']]
PAGINATED_BY = 10

SITE_NAME = os.environ['ATALAKU_SITE_NAME']
META_KEYWORDS = "Event,Events, Africa, Africans, Africains, Evènement, Publicité, publication, party, fête,anniversaire"
META_DESCRIPTION = "ATALAKU est un site de publication des evenements africains qui on lieu n'importe où dans le monde"
# Application definition
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',
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
        #'rest_framework.permissions.IsAdminUser',
        #'rest_framework.permissions.IsAuthenticated',
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.TokenAuthentication',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'production': {
	'ENGINE':   os.environ['ATALAKU_DEFAULT_ENGINE'],
	'NAME'	:   os.environ['ATALAKU_DATABASE_NAME'],
	'USER'	:   os.environ['ATALAKU_DATABASE_USERNAME'],
	'PASSWORD': os.environ['ATALAKU_DATABASE_PW'],
	'HOST'	:   os.environ['ATALAKU_DATABASE_HOST'] ,
	'PORT' 	:   os.environ['ATALAKU_DATABASE_PORT'],
    'OPTIONS' : {
        'sslmode': 'require'
    },
    'TEST'  :   {
        'NAME': 'test_db',
    },
   },

}

DEFAULT_DATABASE = os.environ.get('DJANGO_DATABASE', 'dev')
DATABASES['default'] = DATABASES[DEFAULT_DATABASE]


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
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'console_custom_apps': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },

        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename':'logs/atalaku.log'
        },
        'file_custom_apps': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename':'logs/custom_apps/apps.log'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '' : {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'accounts' : {
            'level': 'DEBUG',
            'handlers': ['console_custom_apps', 'file_custom_apps'],
            'propagate': False,
        },
        'django': {
            'level': 'ERROR',
            'handlers': ['file', 'console'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        }
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
    os.path.join(BASE_DIR, 'conf/locale')
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
