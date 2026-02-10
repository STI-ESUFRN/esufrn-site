import threading
import logging

from django.conf import settings
from django.core.mail import EmailMessage, send_mail

_logger = logging.getLogger(__name__)


def send_mail_async(**kwargs):
    """Call django.core.mail.send_mail in a background thread and log failures.

    This wraps the original behavior but catches and logs exceptions so threads
    don't show uncaught tracebacks in the logs.
    """
    kwargs.setdefault("from_email", settings.EMAIL_HOST_USER)
    kwargs.setdefault("message", "")
    kwargs.setdefault("fail_silently", False)

    def _send():
        try:
            send_mail(**kwargs)
        except Exception:
            _logger.exception("send_mail_async failed")

    threading.Thread(target=_send).start()


def send_email_with_attachments(subject, html_message, recipient_list, attachments=None, from_email=None):
    """
    Envia email com anexos de forma assíncrona.
    
    Args:
        subject: Assunto do email
        html_message: Conteúdo HTML do email
        recipient_list: Lista de destinatários
        attachments: Lista de tuplas (filename, content, mimetype) ou lista de arquivos Django UploadedFile
        from_email: Email do remetente (opcional, usa EMAIL_HOST_USER por padrão)
    """
    if from_email is None:
        from_email = settings.EMAIL_HOST_USER
    
    def _send():
        try:
            email = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=from_email,
                to=recipient_list,
            )
            email.content_subtype = "html"  # Define que o corpo é HTML
            
            # Adicionar anexos
            if attachments:
                for attachment in attachments:
                    if hasattr(attachment, 'read'):  # É um arquivo Django UploadedFile
                        try:
                            email.attach(attachment.name, attachment.read(), attachment.content_type)
                        except Exception:
                            _logger.exception("failed to attach UploadedFile %s", getattr(attachment, 'name', '<unknown>'))
                    elif isinstance(attachment, tuple) and len(attachment) == 3:  # (filename, content, mimetype)
                        email.attach(attachment[0], attachment[1], attachment[2])

            email.send(fail_silently=False)
        except Exception:
            _logger.exception("send_email_with_attachments failed")
    
    threading.Thread(target=_send).start()
