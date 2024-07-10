import os
from pathlib import Path

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

load_dotenv(override=True)


def get_nth_parent(path: Path, parents: int) -> str:
    if not parents:
        return path

    return get_nth_parent(path.parent, parents - 1)


BASE_DIR = get_nth_parent(Path(__file__).resolve(), 3)
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(" ")

INSTALLED_APPS = [
    # other
    "admin_interface",
    "colorfield",
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps
    "assets",
    "principal",
    "dashboard",
    "laboratorio",
    "reserva",
    "chamado",
    "eventos",
    "revistas",
    "menu",
    # lib
    "constance",
    "rest_framework",
    "django_filters",
    "multiselectfield",
    "ckeditor",
    "ckeditor_uploader",
    "corsheaders",
    "mathfilters",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

X_FRAME_OPTIONS = "SAMEORIGIN"

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://* https://*").split(
    " ",
)


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = [
#     "http://barra.brasil.gov.br",
# ]

ROOT_URLCONF = "esufrn.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates", "base"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "menu.context.menu_itens",
                "dashboard.context.navbar",
            ],
        },
    },
]

LOCALE_PATHS = (os.path.join(os.path.dirname(os.path.realpath(__name__)), "locale"),)


WSGI_APPLICATION = "esufrn.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
DATE_FORMAT = "d-m-Y"
DATE_INPUT_FORMATS = ["%d-%m-%Y"]

HOST_URL = "http://escoladesaude.ufrn.br"

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

ADMINS = [
    ("SUPORTE", "suporteeen@gmail.com"),
    ("SUPORTE", "suporte.es@ufrn.br"),

]


BOLD = ""

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": os.getenv(
        "REST_RENDERERS",
        "rest_framework.renderers.JSONRenderer "
        "rest_framework.renderers.BrowsableAPIRenderer",
    ).split(" "),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 8,
}

CONSTANCE_BACKEND = "constance.backends.redisd.RedisBackend"
CORS_ALLOW_HEADERS = list(default_headers) + ["scope"]

CONSTANCE_REDIS_CONNECTION = os.getenv(
    "CONSTANCE_REDIS_CONNECTION",
    "redis://localhost:6379/1",
)

CONSTANCE_CONFIG = {
    "CONTACT_EMAIL": (
        "esufrn@ufrn.br",
        "Contact_Email",
        str,
    ),
    "CONTACT_EMAIL_SUPORTE": (
        "suporte@es.ufrn.br",
        "Contact_Email_Suporte",
        str,
    ),
}

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/2"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "django_orm",
    },
}

# Celery
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"
CELERY_IGNORE_RESULT = False
CELERY_TRACK_STARTED = True
CELERY_TASK_RESULT_EXPIRES = 0
CELERY_TIMEZONE = TIME_ZONE
