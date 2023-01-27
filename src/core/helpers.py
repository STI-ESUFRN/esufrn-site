import threading

from django.conf import settings
from django.core.mail import send_mail


def send_mail_async(**kwargs):
    kwargs.setdefault("from_email", settings.EMAIL_HOST_USER)
    kwargs.setdefault("message", "")
    kwargs.setdefault("fail_silently", False)
    threading.Thread(target=send_mail, kwargs=kwargs).start()
