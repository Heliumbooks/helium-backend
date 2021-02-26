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
ALLOWED_HOSTS = ['https://1ee159583bae.ngrok.io', 'http://1ee159583bae.ngrok.io', '1ee159583bae.ngrok.io', 'localhost',
                 '127.0.0.1']

CORS_ORIGIN_WHITELIST = [
    'https://localhost:3000', 'https://127.0.0.1:3000', 'http://localhost:3000', 'http://127.0.0.1:3000'
]
