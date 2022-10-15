import threading
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Chamado(SoftDeletableModel, TimeStampedModel):
    class Status(models.TextChoices):
        RESOLVED = "Resolved"
        NOT_RESOLVED = "Not resolved"
        PENDING = "Pending"

    title = models.CharField("Título", max_length=100)
    description = models.TextField("Descrição", max_length=300)
    requester = models.CharField("Solicitante", max_length=50)
    course = models.CharField("Curso", max_length=100)
    contact = models.CharField("Whatsapp ou Email", max_length=50)
    date = models.DateTimeField("Registrado em", auto_now=False, auto_now_add=True)
    solved_at = models.DateTimeField("Resolvido em", null=True)
    obs = models.TextField("Observações", null=True)
    status = models.CharField(
        "Status", max_length=12, choices=Status.choices, default=Status.PENDING
    )

    def save(self, *args, **kwargs):
        pk = self.pk

        if self.status is not self.Status.PENDING:
            if self.solved_at is None:
                self.solved_at = datetime.today()
        else:
            self.solved_at = None

        super(Chamado, self).save(*args, **kwargs)

        if pk is None:
            self.notify()

    def notify(self):
        message = """
            Um novo chamado foi cadastrado no sistema.<br/>
            Título: {0}<br/>
            Descrição: {1}<br/>
            Solicitante: {2}<br/>
            Curso: {3}<br/>
            Contato: {4}
        """.format(
            self.title,
            self.description,
            self.requester,
            self.course,
            self.contact,
        )

        context = {"message": message}
        msg = render_to_string("base.email_conversation.html", context)

        threading.Thread(
            target=send_mail,
            args=(
                (
                    "Sistema de Chamados: {0}".format(
                        self.title,
                    ),
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
        ordering = ["-date"]

    def __str__(self):
        return self.title
