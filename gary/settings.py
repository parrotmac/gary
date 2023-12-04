"""
Django settings for gary project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

import dj_database_url


def get_envvar_list(envvar_name, default=[], separator=",", normalize=True):
    env_value = os.getenv(envvar_name)

    if not env_value:
        return default

    results = []
    for val in env_value.split(separator):
        if normalize:
            if val and val.strip() != "":
                results.append(val)
        else:
            results.append(val)
    return results


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-$1u^am(!h^zxcbi=^c1fga=mpv)zaw&lry$na3u*lgovf6jcf9"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "ENABLED") == "ENABLED"

ALLOWED_HOSTS = get_envvar_list("ALLOWED_HOSTS")
TLS_ENABLED = os.getenv("TLS_ENABLED", "ENABLED") == "ENABLED"

# https://docs.djangoproject.com/en/dev/releases/4.0/#format-change
CSRF_TRUSTED_ORIGINS = [
    f"{'https' if TLS_ENABLED else 'http'}://{host}" for host in ALLOWED_HOSTS
]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = get_envvar_list(
    "CORS_ORIGIN_WHITELIST",
    ["https://{}".format(origin) for origin in ALLOWED_HOSTS],
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "gifter.apps.GifterConfig",
    "bootstrap5",
    "whitenoise",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

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

ROOT_URLCONF = "gary.urls"

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
                "django.template.context_processors.request",
            ],
        },
    },
]

APPEND_SLASH = False

WSGI_APPLICATION = "gary.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
    }
}
if database_url := os.getenv("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(conn_max_age=600)


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "gifter.User"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": os.getenv("GOOGLE_AUTH_CLIENT_ID"),
            "secret": os.getenv("GOOGLE_AUTH_SECRET"),
        },
    }
}

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = os.environ.get(
    "DJANGO_STATIC_ROOT", os.path.join(BASE_DIR, "staticfiles")
)

STATICFILES_DIRS = [
    BASE_DIR / "gifter/static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


###
# Email
###
# See https://docs.djangoproject.com/en/4.0/ref/settings/#email-backend

# Will default to root@localhost or webmaster@localhost which will get flagged as spam
# Mostly used fo automated emails, e.g. errors
# Django's Email system allows defining a different 'From' email when manually sending email
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL", "Gary The Wishlist Fairy <noreply@mail.parker.style>"
)

# Used for system generated email, such as Email Address verification
DEFAULT_NOREPLY_EMAIL = os.getenv(
    "DEFAULT_NOREPLY_EMAIL", "Gary The Wishlist Fairy <noreply@mail.parker.style>"
)

# Quickstart from https://sendgrid.com/docs/for-developers/sending-email/django/
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

MAILHOG_HOST = os.getenv("MAILHOG_HOST")

# Let app code check to see if Sendgrid is available
SENDGRID_ENABLED = False

SENDGRID_EMAIL_INVITE_TEMPLATE = os.getenv(
    "SENDGRID_EMAIL_INVITE_TEMPLATE", "d-7d32f3f48de243c6a5438af162ffc6d5"
)

# How long before a second email can be sent from a user to a particular email for a particular group
INVITE_EMAIL_COOLDOWN_PERIOD_MINUTES = os.getenv(
    "INVITE_EMAIL_COOLDOWN_PERIOD_MINUTES", "5"
)

if SENDGRID_API_KEY:
    SENDGRID_ENABLED = True
    # Consider 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
    SENDGRID_SANDBOX_MODE_IN_DEBUG = False
elif MAILHOG_HOST:
    print("Using mailhog", MAILHOG_HOST)
    EMAIL_HOST = MAILHOG_HOST
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False
else:
    # Emails won't be sent unless configured above
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# See https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-ADMINS
ADMINS = [
    # Expects a list of tuples, e.g. ('Mary', 'mary@example.com'),
]

DEFAULT_ADMINS = ["Isaac:isaac@sianware.com"]
for admin in get_envvar_list("ADMINS", DEFAULT_ADMINS):
    if ":" in admin:
        parts = admin.split(":")
        ADMINS.append((parts[0], parts[1]))


###
# Logging
###

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "filters": [],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": [],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "gifter": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

SENTRY_DSN = os.getenv("SENTRY_DSN")

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        # By default the SDK will try to use the SENTRY_RELEASE
        # environment variable, or infer a git commit
        # SHA as release, however you may want to set
        # something more human-readable.
        # release="myapp@1.0.0",
    )
