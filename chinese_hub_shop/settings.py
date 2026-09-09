"""
Django settings for chinese_hub_shop project.
"""

from pathlib import Path
from decimal import Decimal
import os


# =============================================================================
# BASE DIRECTORY
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECURITY
# =========================================================

SECRET_KEY = "jnv2ee%h)guemm@gtjk_gz#9x73=v4sjbu6ntkzf=x#6)jy-wh"

if not SECRET_KEY:
    if os.environ.get("DEBUG", "False").lower() == "true":
        SECRET_KEY = "django-insecure-local-development-key"
    else:
        raise RuntimeError(
            "DJANGO_SECRET_KEY environment variable is not set."
        )


# =========================================================
# DEBUG
# =========================================================

DEBUG = True


# =========================================================
# HOSTS
# =========================================================

ALLOWED_HOSTS = [
    "thechinesehub.vercel.app",
    ".vercel.app",
    "localhost",
    "127.0.0.1",
]


CSRF_TRUSTED_ORIGINS = [
    "https://thechinesehub.vercel.app",
    "https://*.vercel.app",
]
# =============================================================================
# APPLICATIONS
# =============================================================================

INSTALLED_APPS = [
    # Django built-in applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your application
    "shop",
]


# =============================================================================
# MIDDLEWARE
# =============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise serves Django static files
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =============================================================================
# STATIC FILE STORAGE
# =============================================================================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# =============================================================================
# URL CONFIGURATION
# =============================================================================

ROOT_URLCONF = "chinese_hub_shop.urls"


# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # Your custom context processors
                "shop.context_processors.cart_count",
                "shop.context_processors.shop_contact",
            ],
        },
    },
]


# =============================================================================
# WSGI APPLICATION
# =============================================================================

WSGI_APPLICATION = "chinese_hub_shop.wsgi.application"


# =============================================================================
# DATABASE
# =============================================================================
#
# IMPORTANT:
# SQLite is okay for your current testing/deployment setup.
#
# For a production food-ordering website with real customers/orders,
# PostgreSQL is recommended later.
#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# =============================================================================
# STATIC FILES
# =============================================================================
#
# Your actual structure:
#
# static/
# └── shop/
#     ├── css/
#     │   └── style.css
#     └── img/
#

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# =============================================================================
# MEDIA FILES
# =============================================================================
#
# Your actual structure:
#
# media/
# ├── bills/
# └── food_items/
#

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# =============================================================================
# SECURITY / VERCEL HTTPS
# =============================================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# Only use secure cookies in production.
SESSION_COOKIE_SECURE = not DEBUG

CSRF_COOKIE_SECURE = not DEBUG


# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =============================================================================
# SHOP SETTINGS
# =============================================================================

SHOP_NAME = "The Chinese Hub"


# =============================================================================
# OWNER INFORMATION
# =============================================================================

OWNER_NAME = "Sohail Arab"

# Number displayed to customers
OWNER_PHONE_DISPLAY = "7757855545"

# Number used by tel: links
OWNER_PHONE_TEL = "7757855545"


# =============================================================================
# WHATSAPP
# =============================================================================
#
# India:
# +91 7757855545
#
# WhatsApp format:
# 917757855545
#
# No + sign
# No spaces
# No hyphens
#

OWNER_WHATSAPP_NUMBER = "917757855545"


# =============================================================================
# BILLING
# =============================================================================

# Flat service charge added to every order.

SERVICE_CHARGE = Decimal("0.00")