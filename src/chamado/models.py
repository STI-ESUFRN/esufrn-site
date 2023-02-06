import threading
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Chamado(SoftDeletableModel, TimeStampedModel):
    class Status(models.TextChoices):
        RESOLVED = "R", _("Resolved")
        NOT_RESOLVED = "N", _("Not resolved")
        PENDING = "P", _("Pending")

    title = models.CharField("Título", max_length=100)
    description = models.TextField("Descrição", max_length=300)
    requester = models.CharField("Solicitante", max_length=50)
    course = models.CharField("Curso", max_length=100)
    contact = models.CharField("Whatsapp ou Email", max_length=50)
    solved_at = models.DateTimeField("Resolvido em", null=True)
    obs = models.TextField("Observações", null=True)
    status = models.CharField(
        "Status", max_length=1, choices=Status.choices, default=Status.PENDING
    )

    def save(self, *args, **kwargs):
        pk = self.pk

        if self.status is not self.Status.PENDING:
            if self.solved_at is None:
                self.solved_at = datetime.today()
        else:
            self.solved_at = None

        super().save(*args, **kwargs)

        if pk is None:
            self.notify()

    def notify(self):
        message = f"""
            Um novo chamado foi cadastrado no sistema.<br/>
            Título: {self.title}<br/>
            Descrição: {self.description}<br/>
            Solicitante: {self.requester}<br/>
            Curso: {self.course}<br/>
            Contato: {self.contact}
        """

        context = {"message": message}
        msg = render_to_string("base.email_conversation.html", context)

        threading.Thread(
            target=send_mail,
            args=(
                (
                    f"Sistema de Chamados: {self.title}",
                    "",
                    settings.EMAIL_HOST_USER,
                    [settings.CONTACT_EMAIL_SUPORTE],
                    False,
                    None,
                    None,
                    None,
                    msg,
                )
            ),
        ).start()

    class Meta:
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        ordering = ["-created"]

    def __str__(self):
        return self.title
