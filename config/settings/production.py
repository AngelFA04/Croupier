import os

import dj_database_url

from .base import *  # noqa
from .base import env

INSTALLED_APPS += ["whitenoise.runserver_nostatic"]  # noqa

ALLOWED_HOSTS = ["127.0.0.1", ".herokuapp.com"]
DEBUG = False

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {"default": env.db("DATABASE_URL", default="postgres://")}
