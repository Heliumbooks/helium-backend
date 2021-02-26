from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'degk73g0rh4loi',
        'USER': 'mfwhvnlcxjsbzc',
        'PASSWORD': '821b6b2f40433eab52795baef2df494dfac6b9c4cfc9b863a6fd0ed305331d0d',
        'HOST': 'ec2-52-205-3-3.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

DEBUG = False

CORS_ORIGIN_WHITELIST = [
    'https://localhost:3000', 'https://127.0.0.1:3000', 'http://localhost:3000', 'http://127.0.0.1:3000',
    "https://helium-frontend.herokuapp.com"
]

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', 'helium-django-backend.herokuapp.com']