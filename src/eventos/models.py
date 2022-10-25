from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Event(SoftDeletableModel, TimeStampedModel):
    name = models.CharField("Nome do evento", max_length=255)
    image = models.ForeignKey(
        "assets.ESImage", verbose_name="Imagem", on_delete=models.PROTECT
    )
    date_begin = models.DateField("Data de início")
    date_end = models.DateField("Data de término")
    local = models.CharField("Local", max_length=255, default="A Definir")
    contact = models.EmailField("Email", max_length=255, null=True, blank=True)
    coordination = models.CharField("Coordenação", max_length=255)
    target = models.TextField("Público alvo", null=True)

    class Meta:
        ordering = ["-created"]


class AdditionalInformation(models.Model):
    event = models.ForeignKey(
        Event, related_name="informations", on_delete=models.CASCADE
    )
    name = models.CharField("Informação", max_length=255)
    details = RichTextUploadingField("Detalhes")

    class Meta:
        ordering = ["event__id", "name"]


class Attachment(TimeStampedModel):
    event = models.ForeignKey(
        Event, related_name="attachments", on_delete=models.CASCADE
    )
    file = models.ForeignKey("assets.File", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]
