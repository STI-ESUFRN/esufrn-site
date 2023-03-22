from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from model_utils.models import SoftDeletableModel, TimeStampedModel

from assets.models import File


class Event(SoftDeletableModel, TimeStampedModel):
    name = models.CharField("Nome do evento", max_length=255)
    image = models.ForeignKey(
        "assets.ESImage",
        verbose_name="Imagem",
        on_delete=models.PROTECT,
    )
    date_begin = models.DateField("Data de início")
    date_end = models.DateField("Data de término")
    local = models.CharField("Local", max_length=255, default="A Definir")
    contact = models.EmailField("Email", max_length=255, null=True, blank=True)
    coordination = models.CharField("Coordenação", max_length=255)
    target = models.TextField("Público alvo", null=True)
    slug = models.SlugField(
        "Atalho",
        max_length=255,
        help_text=(
            "Este campo será preenchido automaticamente, ele representa a URL do"
            " evento. Ele é único e nenhum outro evento deverá ter o mesmo atalho."
        ),
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.name}-{self.created.date()}")

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("evento", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-created"]
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self) -> str:
        return self.name


class AdditionalInformation(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="informations",
        on_delete=models.CASCADE,
    )
    name = models.CharField("Informação", max_length=255)
    details = RichTextUploadingField("Detalhes", config_name="events")

    def __str__(self) -> str:
        return f"{self.event}|{self.name}"

    class Meta:
        ordering = ["event__id", "name"]
        verbose_name = "Informação adicional"
        verbose_name_plural = "Informações adicionais"


class Attachment(File):
    event = models.ForeignKey(
        Event,
        related_name="attachments",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
