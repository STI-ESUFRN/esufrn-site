import sys
from io import BytesIO

import qrcode
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from model_utils.models import SoftDeletableModel, TimeStampedModel

from assets.models import ESImage


class Material(TimeStampedModel, SoftDeletableModel):
    class Type(models.TextChoices):
        DURABLE = "D", "Durável"
        CONSUMABLE = "C", "Consumível"

    name = models.CharField("Nome", max_length=255)
    expiration = models.DateField("Data de validade", null=True, blank=True)
    type = models.CharField("Tipo", choices=Type.choices, max_length=1)
    quantity = models.IntegerField("Quantidade disponível")
    received_date = models.DateField("Recebido em")
    qr = models.ForeignKey(
        "assets.ESImage", on_delete=models.PROTECT, null=True, editable=False
    )

    def generate_qr(self, request):
        qr = qrcode.make(
            request.build_absolute_uri(
                reverse("almoxarifado:materials-detail", kwargs={"pk": self.id})
            )
        )
        stream = BytesIO()
        qr.save(stream, format="PNG", optimize=True)

        stream.seek(0)
        image = InMemoryUploadedFile(
            stream,
            "ImageField",
            f"{self.id}-{self.name}-{self.created}.png",
            "image/png",
            sys.getsizeof(stream),
            None,
        )
        self.qr = ESImage.objects.create(high=image)

        self.save()

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"
        ordering = ["-created"]
