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
    type = models.CharField("Tipo", choices=Type.choices, max_length=1)
    alert_below = models.IntegerField("Nível crítico", null=True, blank=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"
        ordering = ["-created"]


class MaterialInstance(TimeStampedModel):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    expiration = models.DateField("Data de validade", null=True, blank=True)
    quantity = models.IntegerField("Quantidade disponível")
    qr = models.ForeignKey(
        "assets.ESImage", on_delete=models.PROTECT, null=True, editable=False
    )

    def generate_qr(self, request):
        qr = qrcode.make(
            request.build_absolute_uri(
                reverse("almoxarifado_editar", kwargs={"pk": self.id})
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
        verbose_name = "Instância"
        verbose_name_plural = "Instâncias"
        ordering = ["-created"]


class History(TimeStampedModel):
    class TypeChoices(models.TextChoices):
        REMOVAL = "R", "Remoção"
        ADDITION = "A", "Adição"

    instance = models.ForeignKey(MaterialInstance, on_delete=models.CASCADE)
    quantity = models.IntegerField("Quantidade disponível")
    type = models.CharField("Tipo", max_length=1, choices=TypeChoices.choices)

    class Meta:
        verbose_name = "Histórico de material"
        verbose_name_plural = "Histórico de materiais"
        ordering = ["instance__id", "-created"]
