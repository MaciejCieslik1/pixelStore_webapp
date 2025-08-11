from .settings import *

import os

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store.apps.StoreConfig',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME', 'pixelStore_test_db'),
        'USER': os.getenv('DATABASE_USER', 'student'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'student'),
        'HOST': os.getenv('DATABASE_HOST', 'database'),
        'PORT': os.getenv('DATABASE_PORT', '3306'),
        'TEST': {
            'NAME': os.getenv('DATABASE_NAME', 'pixelStore_test_db'),
            'CREATE_DB': False
        },
    }
}


DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
