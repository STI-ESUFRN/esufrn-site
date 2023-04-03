from django.contrib.auth.models import User
from django.template.loader import render_to_string

from core.helpers import send_mail_async


def send_alert_email(material, *args, **kwargs):
    subject = (
        f"Material em nível crítico {material.name}: Restam apenas {material.quantity}"
    )

    message = render_to_string(
        "laboratorio/consumivel/email.html",
        {"material": material},
    )

    html = render_to_string("base.email_conversation.html", {"message": message})

    responsibles = User.objects.filter(groups__name="laboratorio")
    recipient_list = [recipient.user.email for recipient in responsibles]
    send_mail_async(
        subject=subject,
        recipient_list=recipient_list,
        html_message=html,
    )
