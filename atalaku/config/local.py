from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
    'local': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'atalaku.sqlite3',
    },
}

