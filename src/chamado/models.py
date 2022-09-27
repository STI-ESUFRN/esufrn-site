import threading
from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string


class Chamado(models.Model):
    title = models.CharField("Título", max_length=100)
    description = models.CharField("Descrição", max_length=300, null=True, blank=True)
    requester = models.CharField("Solicitante", max_length=50)
    course = models.CharField("Curso", max_length=100)
    contact = models.CharField(
        "Whatsapp ou Email", max_length=50, null=True, blank=True
    )
    date = models.DateTimeField("Registrado em", auto_now=False, auto_now_add=True)
    solved_at = models.DateTimeField("Resolvido em", null=True, blank=True)
    lastModified = models.DateTimeField("Última modificação", auto_now=True)

    obs = models.TextField("Observações", null=True, blank=True)
    status = models.BooleanField("Status", null=True)

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

    def save(self, *args, **kwargs):
        pk = self.pk

        if self.status is not None:
            if self.solved_at is None:
                self.solved_at = datetime.today()
        else:
            self.solved_at = None

        super(Chamado, self).save(*args, **kwargs)

        if pk is None:
            self.notify()

    class Meta:
        verbose_name = "Chamado"
        verbose_name_plural = "Chamados"
        ordering = ["-date"]

    def __str__(self):
        return self.title
