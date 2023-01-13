import sys
from io import BytesIO

import qrcode
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from model_utils.models import SoftDeletableModel, TimeStampedModel

from assets.models import ESImage


class Material(SoftDeletableModel, TimeStampedModel):
    name = models.CharField("Nome", max_length=255)
    description = models.TextField("Descrição")
    brand = models.CharField("Marca", max_length=255, null=True, blank=True)
    received_at = models.DateField("Recebido em", null=True, blank=True)
    location = models.CharField("Localização", max_length=255, null=True, blank=True)
    comments = models.TextField("Observações", null=True, blank=True)
    qr_code = models.ForeignKey(
        "assets.ESImage", on_delete=models.PROTECT, null=True, editable=False
    )

    class Meta:
        verbose_name = "Instância"
        verbose_name_plural = "Instâncias"
        ordering = ["-created"]

    def get_url(self) -> str:
        raise NotImplementedError

    def generate_qr(self, request):
        qr_code = qrcode.make(request.build_absolute_uri(self.get_url()))
        stream = BytesIO()
        qr_code.save(stream, format="PNG", optimize=True)

        stream.seek(0)
        image = InMemoryUploadedFile(
            stream,
            "ImageField",
            f"{self.id}-{self.name}-{self.created}.png",
            "image/png",
            sys.getsizeof(stream),
            None,
        )
        self.qr_code = ESImage.objects.create(high=image)

        self.save()


class Consumable(Material):
    expiration = models.DateField("Data de validade", null=True, blank=True)
    alert_below = models.IntegerField("Nível crítico", null=True, blank=True)
    reference = models.IntegerField("Valor de referência", null=True, blank=True)
    quantity = models.IntegerField("Quantidade disponível")

    @property
    def warn(self):
        return self.quantity / (self.reference - self.alert_below) < 0.40

    @property
    def relative_percentage(self):
        return int(self.quantity / self.reference * 100)

    class Meta:
        verbose_name = "Material permanente"
        verbose_name_plural = "Materiais permanentes"
        ordering = ["-created"]

    def get_url(self):
        return reverse("material_editar", kwargs={"pk": self.id})

    def create_log(self, request, **kwargs):
        if not self.pk:
            History.objects.create(
                user=request.user,
                item=self,
                quantity=self.quantity,
            )

        else:
            obj = Consumable.objects.get(id=self.id)
            if obj.quantity != self.quantity:
                History.objects.create(
                    user=request.user,
                    item=self,
                    quantity=self.quantity,
                    prev_quantity=obj.quantity,
                )


class History(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="history")
    quantity = models.IntegerField("Quantidade atualizada")
    prev_quantity = models.IntegerField("Quantidade anterior", default=0)

    @property
    def diff(self):
        return self.quantity - self.prev_quantity

    class Meta:
        verbose_name = "Histórico de material"
        verbose_name_plural = "Histórico de materiais"
        ordering = ["item__id", "-created"]


class Category(models.Model):
    name = models.TextField("Nome", max_length=255)
    description = models.TextField("Descrição", null=True, blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Permanent(Material):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Disponível"
        UNAVAILABLE = "UNAVAILABLE", "Indisponível"

    number = models.CharField("Tombamento", max_length=255, unique=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)
    status = models.CharField(
        "Status", max_length=11, choices=Status.choices, default=Status.AVAILABLE
    )

    class Meta:
        verbose_name = "Material permanente"
        verbose_name_plural = "Materiais permanentes"
        ordering = ["-created"]

    def get_url(self):
        return reverse("material_editar", kwargs={"pk": self.id})
