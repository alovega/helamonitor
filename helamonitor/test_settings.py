"""
The test settings for Helamonitor.
"""
from helamonitor.settings import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
