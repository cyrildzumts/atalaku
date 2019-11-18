from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
    'TEST'  :   {
        'NAME': 'test_db',
    },
   },

}

DEFAULT_DATABASE = os.environ.get('DJANGO_DATABASE', 'dev')
DATABASES['default'] = DATABASES[DEFAULT_DATABASE]