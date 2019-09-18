# coding=utf-8
"""
The Jenkins test settings for HelaMonitor project
"""
from .settings import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
	}
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
LOGGING = {}
FILE_CONTENT_ROOT = BASE_DIR
STATIC_ROOT = BASE_DIR
