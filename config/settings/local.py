# Import base settings
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'heliumapi',
        'USER': 'charles',
        'PASSWORD': 'Password1!',
        'HOST': 'localhost',
        'PORT': '',
    }
}

DEBUG = True

"""
Remove the allowed hosts from prod
"""
ALLOWED_HOSTS = []