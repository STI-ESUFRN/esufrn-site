import os

from django.db import models
from model_utils.models import TimeStampedModel

from assets.helpers import Quality, resize_image


class ESImage(TimeStampedModel):
    high = models.ImageField("Imagem (qualidade original)", upload_to="images")
    medium = models.ImageField(
        "Imagem (qualidade média)", blank=True, null=True, upload_to="images"
    )
    low = models.ImageField(
        "Imagem (qualidade baixa)", blank=True, null=True, upload_to="images"
    )

    def save(self, *args, **kwargs):
        self.medium = resize_image(self.high, quality=Quality.MEDIUM)
        self.low = resize_image(self.high, quality=Quality.WORSE)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Imagem"
        verbose_name_plural = "Imagens"
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"{os.path.basename(self.high.name)}"


class File(TimeStampedModel):
    url = models.FileField(upload_to="files")

    def filename(self) -> str:
        return os.path.basename(self.url.name)

    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.filename()}"
