import threading

from constance import config
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Chamado(SoftDeletableModel, TimeStampedModel):
    class Status(models.TextChoices):
        RESOLVED = "R", _("Resolved")
        NOT_RESOLVED = "N", _("Not resolved")
        PENDING = "P", _("Pending")

    class Shift(models.TextChoices):
        MORNING = "M", "Manhã"
        AFTERNOON = "T", "Tarde"

    class Concorda(models.TextChoices):
        YES = "y", "SIM"

    title = models.CharField("Título", max_length=100)
    description = models.TextField("Descrição do problema", max_length=300)
    requester = models.CharField("Nome completo", max_length=50)
    course = models.CharField("Nome do curso", max_length=100)
    contact = models.CharField("Whatsapp ou Email para contato", max_length=50)
    presenca = models.BooleanField(
        "Supervisionado por docente",
        default=False,
        help_text=(
            "Marcando esta caixa, você declara que a sala contará com a supervisão de"
            " um docente no momento da aula."
        ),
    )
    date = models.DateField("Data *", null=True)
    shift = models.CharField(
        "Turno *",
        max_length=10,
        choices=Shift.choices,
        null=True,
    )
    concorda = models.CharField(
        "Marcando esta caixa você declara que estará presente no momento da manutenção",
        max_length=10,
        choices=Concorda.choices,
    )
    solved_at = models.DateTimeField("Resolvido em", null=True)
    obs = models.TextField("Observações", null=True)
    status = models.CharField(
        "Status",
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def save(self, *args, **kwargs):
        pk = self.pk

        if self.status is not self.Status.PENDING:
            if self.solved_at is None:
                self.solved_at = timezone.now()
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
            Contato: {self.contact}<br/>
            Data: {self.date}<br/>
            Turno: {self.shift}
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
                    [config.CONTACT_EMAIL_SUPORTE],
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
