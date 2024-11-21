import os
import dj_database_url
from pathlib import Path
from configurations import Configuration, values

class Dev(Configuration):

    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = "django-insecure-+7v=+t$9p4n%1p6mfy9v+sx3)f_&y&)(wswgz06&w@nl8d8ers"

    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = values.ListValue([
        "0.0.0.0",
        "127.0.0.1",
    ])

    INSTALLED_APPS = [
        # "django.contrib.admin",
        # "reviewsapp.apps.ReviewsappAdminConfig",
        "bookr_admin.apps.BookrAdminConfig",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "reviewsapp.apps.ReviewsappConfig",
        "book_management.apps.BookManagementConfig",
        "rest_framework",
        "rest_framework.authtoken",
        "crispy_forms",
        "crispy_bootstrap4",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "config.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "templates")],
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

    WSGI_APPLICATION = "config.wsgi.application"

    DATABASES = values.DatabaseURLValue('sqlite:///{}/db.sqlite3'.format(BASE_DIR), environ_prefix='DJANGO')

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

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    STATIC_URL = "static/"
    # STATIC_ROOT = BASE_DIR / "static/"
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

    MEDIA_URL = "media/"
    MEDIA_ROOT = BASE_DIR / "media"

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    CRISPY_TEMPLATE_PACK = "bootstrap4"


class Prod(Dev):
    DEBUG = False
    SECRET_KEY = values.SecretValue()