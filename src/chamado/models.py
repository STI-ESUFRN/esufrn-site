import threading

from constance import config
from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Sala(models.Model):
    nome = models.CharField("Sala", max_length=100, unique=True)

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Chamado(SoftDeletableModel, TimeStampedModel):
    class Status(models.TextChoices):
        RESOLVED = "R", _("Resolved")
        NOT_RESOLVED = "N", _("Not resolved")
        PENDING = "P", _("Pending")

    equipment = models.CharField("Equipamento", max_length=100)
    description = models.TextField("Descrição do problema", max_length=300)
    requester = models.CharField("Solicitante", max_length=50)
    sala = models.ForeignKey(
        Sala,
        verbose_name="Sala",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="chamados",
    )
    sala_outros = models.CharField("Sala (outros)", max_length=100, blank=True, default="")
    tombamento = models.CharField("Tombamento", max_length=100)
    date = models.DateField("Data", null=True)
    responsible_technician = models.CharField(
        "Responsável técnico",
        max_length=100,
        blank=True,
        default="",
    )
    solved_at = models.DateTimeField("Resolvido em", null=True)
    obs = models.TextField("Observações", null=True, blank=True)
    status = models.CharField(
        "Status",
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    @property
    def room(self):
        if self.sala is not None:
            return self.sala.nome

        return self.sala_outros

    def get_room_display(self):
        return self.room or "---"

    def save(self, *args, **kwargs):
        pk = self.pk

        if self.status != self.Status.PENDING:
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
            Equipamento: {self.equipment}<br/>
            Tombamento: {self.tombamento}<br/>
            Descrição: {self.description}<br/>
            Solicitante: {self.requester}<br/>
            Sala: {self.get_room_display()}<br/>
            Data: {self.date}<br/>
            Responsável técnico: {self.responsible_technician}
        """

        context = {"message": message}
        msg = render_to_string("base.email_conversation.html", context)

        threading.Thread(
            target=send_mail,
            args=(
                (
                    f"Sistema de Chamados: {self.equipment}",
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
        return self.equipment
