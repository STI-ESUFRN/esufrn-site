import threading

from django.core.mail import send_mail


def send_mail_async(*args, **kwargs):
    threading.Thread(send_mail, *args, **kwargs).start()
