"""
Django settings for helium_backend project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from os import environ, path

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


def root(*dirs):
    base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    return path.join(base_dir, *dirs, '')


SECRET_KEY = get_env_variable('SECRET_KEY')
FIELD_ENCRYPTION_KEY = get_env_variable('FIELD_ENCRYPTION_KEY')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'encrypted_model_fields',
]

LOCAL_APPS = [
    'helium_backend.books.apps.BooksConfig',
    'helium_backend.customers.apps.CustomersConfig',
    'helium_backend.locations.apps.LocationsConfig',
    'helium_backend.orders.apps.OrdersConfig',
    'helium_backend.stripe.apps.StripeConfig',
    'helium_backend.users.apps.UsersConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = ['https://localhost:3000']

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root('helium_backend', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    }
]

AUTH_USER_MODEL = 'users.User'

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [root('helium_backend', 'static')]
STATIC_ROOT = root('helium_backend', 'staticfiles')
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = root('helium_backend', 'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'helium_backend.authentication.authentication.BearerTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

STRIPE_PUBLISHABLE_KEY = 'pk_test_m8cU0zYfxEotRifJeK0F6AzF00rlEKXP0U'
STRIPE_SECRET_KEY = 'sk_test_B8y4EWSJ7zrQWXmXWS5HWJ8Z00NdKOBLlF'
