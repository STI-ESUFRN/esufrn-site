import os

from dotenv import load_dotenv

load_dotenv(override=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = int(os.getenv("DEBUG", True))
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(" ")

HTML_MINIFY = int(os.getenv("MINIFY", False))

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
    " "
)
CSRF_COOKIE_SECURE = int(os.getenv("CSRF_COOKIE_SECURE", False))
SESSION_COOKIE_SECURE = int(os.getenv("SESSION_COOKIE_SECURE", False))

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
                "menu.context.menuItens",
                "dashboard.context.dashboardMenuItens",
            ]
        },
    }
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
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        )
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


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": [
            [
                "Undo",
                "Redo",
                "-",
                "Format",
                "-",
                "Bold",
                "Italic",
                "Underline",
                "Image",
                "HorizontalRule",
                "-",
                "Link",
                "Unlink",
                "-",
                "Cut",
                "Copy",
                "PasteText",
                "-",
                "Subscript",
                "Superscript",
                "SpecialChar",
                "-",
                "Outdent",
                "Indent",
                "-",
                "BulletedList",
                "NumberedList",
            ]
        ],
        "width": "100%",
        "height": 500,
        "toolbarCanCollapse": False,
        "entities_latin": False,
        "basicEntities": False,
    },
    "events": {
        "toolbar": [
            [
                "Undo",
                "Redo",
                "-",
                "Format",
                "-",
                "Bold",
                "Italic",
                "Underline",
                "Image",
                "HorizontalRule",
                "-",
                "Link",
                "Unlink",
                "-",
                "Cut",
                "Copy",
                "PasteText",
                "-",
                "Subscript",
                "Superscript",
                "SpecialChar",
                "-",
                "Outdent",
                "Indent",
                "-",
                "BulletedList",
                "NumberedList",
            ]
        ],
        "width": "100%",
        "height": 180,
        "toolbarCanCollapse": False,
        "entities_latin": False,
        "basicEntities": False,
    },
    "page": {
        "removePlugins": "stylesheetparser",
        "allowedContent": True,
        "toolbar": [
            [
                "Source",
                "Preview",
                "Undo",
                "Redo",
                "-",
                "Format",
                "Font",
                "FontSize",
                "-",
                "Bold",
                "Italic",
                "Underline",
                "Image",
                "HorizontalRule",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
                "-",
                "Link",
                "Unlink",
                "-",
                "Cut",
                "Copy",
                "Paste",
                "PasteText",
                "-",
                "Subscript",
                "Superscript",
                "SpecialChar",
                "-",
                "Outdent",
                "Indent",
                "-",
                "BulletedList",
                "NumberedList",
                "-",
            ]
        ],
        "width": "100%",
        "height": 600,
        "toolbarCanCollapse": False,
        "extraPlugins": ",".join(["codesnippet", "codesnippetgeshi", "div"]),
        "codeSnippet_theme": "railscasts",
        "entities_latin": False,
        "basicEntities": False,
    },
}

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"

ADMINS = [
    ("SUPORTE", "suporteeen@gmail.com"),
    ("SUPORTE", "suporte.es@ufrn.br"),
    ("Felipe", "felipe.medeiros.712@ufrn.edu.br"),
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", default="")

CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")
CONTACT_EMAIL_SUPORTE = os.getenv("CONTACT_EMAIL_SUPORTE")

BOLD = ""

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": os.getenv(
        "REST_RENDERERS",
        (
            "rest_framework.renderers.JSONRenderer "
            "rest_framework.renderers.BrowsableAPIRenderer"
        ),
    ).split(" "),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 8,
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
    }
}
