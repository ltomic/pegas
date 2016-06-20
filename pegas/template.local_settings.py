#Lokalne postavke

import os

ADMINS = ()
MANAGERS = ADMINS

ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don'r run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# Database

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'setname',
		'USER': 'setuser',
		'PASSWORD': 'setpassword',
		'HOST': '',
		'PORT': '',
	}
}

