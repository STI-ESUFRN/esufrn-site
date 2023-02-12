DEBUG = False
HTML_MINIFY = True

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
