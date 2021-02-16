from .base import *
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

DEBUG = True

MIDDLEWARE = MIDDLEWARE + ['whitenoise.middleware.WhiteNoiseMiddleware']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ALLOWED_HOSTS = ['*']

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True