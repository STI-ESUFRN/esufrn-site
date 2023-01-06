import sys
from io import BytesIO

import qrcode
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel

from assets.models import ESImage


class Material(TimeStampedModel):
    class Types(models.TextChoices):
        PERMANENT = "P", "Permanente"
        CONSUMABLE = "C", "Consumível"

    name = models.CharField("Nome", max_length=255)
    description = models.TextField("Descrição")
    quantity = models.IntegerField("Quantidade disponível")
    brand = models.CharField("Marca", max_length=255, null=True, blank=True)
    number = models.CharField("Tombamento", max_length=255, null=True, blank=True)
    expiration = models.DateField("Data de validade", null=True, blank=True)
    received_at = models.DateField("Recebido em", null=True, blank=True)
    alert_below = models.IntegerField("Nível crítico", null=True, blank=True)
    reference = models.IntegerField("Valor de referência", null=True, blank=True)
    location = models.CharField("Localização", max_length=255, null=True, blank=True)
    type = models.CharField(
        "Tipo do material",
        choices=Types.choices,
        default=Types.CONSUMABLE,
        max_length=1,
    )

    qr = models.ForeignKey(
        "assets.ESImage", on_delete=models.PROTECT, null=True, editable=False
    )

    def generate_qr(self, request):
        qr = qrcode.make(
            request.build_absolute_uri(
                reverse("material_editar", kwargs={"pk": self.id})
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

    @property
    def warn(self):
        return self.quantity / (self.reference - self.alert_below) < 0.40

    @property
    def relative_percentage(self):
        return int(self.quantity / self.reference * 100)

    class Meta:
        verbose_name = "Instância"
        verbose_name_plural = "Instâncias"
        ordering = ["-created"]

    def create_log(self, request, **kwargs):
        if not self.pk:
            History.objects.create(
                user=request.user,
                item=self,
                quantity=self.quantity,
            )

        else:
            obj = Material.objects.get(id=self.id)
            quantity = self.quantity - obj.quantity
            if quantity:
                History.objects.create(
                    user=request.user,
                    item=self,
                    quantity=quantity,
                )


class History(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="history")
    quantity = models.IntegerField("Quantidade disponível")

    class Meta:
        verbose_name = "Histórico de material"
        verbose_name_plural = "Histórico de materiais"
        ordering = ["item__id", "-created"]
