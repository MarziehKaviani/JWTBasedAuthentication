from pathlib import Path

import pika
from decouple import config
from django.utils.translation import gettext_lazy as _

import redis
from authentication.settings import *
from common.settings import *
from common.variables import IS_REDIRECT

# Celery
BROKER_URL = os.environ.get(
    'RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')

rabbitmq_user = "guest"
rabbitmq_pass = "guest"
rabbitmq_host = "rabbitmq"
rabbitmq_port = 5672


class RabbitMQConnection:
    def connect(self):
        print('Start Connecting to RabbitMQ...')
        url = config('RABBITMQ_URL', cast=str),
        params = pika.URLParameters(url[0])
        connection = pika.BlockingConnection(params)
        return connection


class RedisConnection:
    # TODO add user pass to redis
    REDIS_PORT = config("REDIS_PORT", cast=str)
    REDIS_HOST = config("REDIS_HOST", cast=str)

    def connect(self):
        print('Start Connecting to Redis...')
        connection = redis.StrictRedis(
            host=self.REDIS_HOST, port=self.REDIS_PORT, decode_responses=True)
        return connection


# RABBIT_MQ_CONNECTION = RabbitMQConnection().connect()
REDIS_CLIENT = RedisConnection().connect()

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "46.249.99.102",
                 "JWTBasedAuthentication.co", "www.JWTBasedAuthentication.co"]
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

IS_REDIRECT_SSL = config(IS_REDIRECT, default=False, cast=bool)
if IS_REDIRECT_SSL:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

# Application definition

INSTALLED_APPS = [
    'modeltranslation',  # model translation needs to be at first

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'celery',
    'django_extensions',
    "drf_yasg",
    "rest_framework",
    "rest_framework_simplejwt",
    'cities_light',

    "home",
    "core",
    "authentication",
    "templates",
]

AUTH_USER_MODEL = "authentication.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "JWTBasedAuthentication.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "JWTBasedAuthentication.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# 'PASSWORD': config('POSTGRES_PASSWORD', default='1qaz!QAZ', cast=str),
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='citizix_db', cast=str),
        'USER': config('POSTGRES_USER', default='citizix_user'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='S3cret', cast=str),
        'HOST': config('DATABASE_HOST', default='postgres', cast=str),
        'PORT': config('DATABASE_PORT', default='5432', cast=str),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]

LANGUAGE_CODE = 'fa'

AVAILABLE_LANGUAGES = ['fa', 'en']
MODELTRANSLATION_LANGUAGES = [
    'fa',
    'en',
]

DEFAULT_LANGUAGE = 'fa'
MODELTRANSLATION_DEFAULT_LANGUAGE = 'fa'
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'fa'
