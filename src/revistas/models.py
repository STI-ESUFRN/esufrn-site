from django.db import models
from django.forms import ValidationError
from model_utils.models import SoftDeletableModel, TimeStampedModel

from core.validators import year_validator


class Revista(SoftDeletableModel, TimeStampedModel):
    class Type(models.TextChoices):
        LINK = "LNK", "Link"
        DOCUMENT = "DOC", "Documento"

    type = models.CharField("Tipo", max_length=3, choices=Type.choices)
    year = models.IntegerField("Ano", validators=[year_validator])
    subtitle = models.CharField("Subtítulo", max_length=255)
    image = models.ForeignKey(
        "assets.ESImage", verbose_name="Capa da revista", on_delete=models.PROTECT
    )
    link = models.CharField("Link", null=True, blank=True, max_length=255)
    file = models.ForeignKey(
        "assets.File",
        verbose_name="Arquivo",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if self.type == self.Type.DOCUMENT and not self.file:
            raise ValidationError(
                "Este tipo de revista requer que seja especificado um arquivo"
            )
        if self.type == self.Type.LINK and not self.link:
            raise ValidationError(
                "Este tipo de revista requer que seja especificado um link"
            )

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
