"""
Django settings for ea project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ConfigParser

config = ConfigParser.ConfigParser()
CFG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "eaconfig.cfg")
config.read(CFG_PATH)

CONFIG = config
BASE_DIR = config.get('paths', 'root')
os.chdir(BASE_DIR)

DEBUG = True if config.get('options', 'debug').lower() == "true" else False
STATIC_ROOT = config.get("paths", "static")

LOGIN_URL = "/login"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get("options", "secret_key")

ALLOWED_HOSTS = [config.get("options", "hostname")]

# Only matters if captcha is integrated
RECAPTCHA_USE_SSL = True

if config.has_section("recaptcha"):
    RECAPTCHA_ENABLED = True
    recaptcha = {k: v for k, v in config.items("recaptcha")}
    RECAPTCHA_PUBLIC_KEY = recaptcha.get("site_key", None)
    if RECAPTCHA_PUBLIC_KEY is None:
        RECAPTCHA_ENABLED = False
    else:
        RECAPTCHA_PRIVATE_KEY = recaptcha.get("secret_key", None)
        if RECAPTCHA_PRIVATE_KEY is None:
            RECAPTCHA_ENABLED = False
    RECAPTCHA_USE_SSL = True
else:
    RECAPTCHA_ENABLED = False

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'exploratory_analysis',
    'ea_services',
)

if RECAPTCHA_ENABLED:
    INSTALLED_APPS = INSTALLED_APPS + ("captcha",)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'ea.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'ea.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

db = {
    "ENGINE": '',
    "NAME": '',
    "HOST": '',
}

db_conf = config.items("database")
for key, val in db_conf:
    db[key.upper()] = val

DATABASES = {
    'default': db
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger"
}
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

import logging

logger = logging.getLogger('exploratory_analysis')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)



