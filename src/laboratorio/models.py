import sys
from io import BytesIO

import qrcode
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from model_utils.models import SoftDeletableModel, TimeStampedModel
from PIL import ImageOps

from assets.models import ESImage
from laboratorio.helpers import send_alert_email
from laboratorio.managers import ConsumableManager


class Warehouse(SoftDeletableModel):
    name = models.CharField("Nome", max_length=255)

    class Meta:
        verbose_name = "Almoxarifado"
        verbose_name_plural = "Almoxarifados"

    def __str__(self) -> str:
        return f"{self.name}"


class UserWarehouse(models.Model):
    user = models.ForeignKey(User, related_name="warehouses", on_delete=models.CASCADE)
    warehouse = models.ForeignKey(
        Warehouse,
        related_name="responsibles",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"
        unique_together = ["user", "warehouse"]

    def __str__(self) -> str:
        return f"{self.user}|{self.warehouse}"


class Material(SoftDeletableModel, TimeStampedModel):
    name = models.CharField("Nome", max_length=255)
    description = models.TextField("Descrição")
    brand = models.CharField("Marca", max_length=255, null=True, blank=True)
    received_at = models.DateField("Recebido em", null=True, blank=True)
    location = models.CharField("Localização", max_length=255, null=True, blank=True)
    comments = models.TextField("Observações", null=True, blank=True)
    qr_code = models.ForeignKey(
        "assets.ESImage",
        on_delete=models.PROTECT,
        null=True,
        editable=False,
    )
    warehouse = models.ForeignKey(
        Warehouse,
        related_name="materials",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"
        ordering = ["name", "-created"]

    def get_url(self) -> str:
        raise NotImplementedError

    def generate_qr(self, request):
        data = request.build_absolute_uri(self.get_url())
        border = (10, 10, 10, 10)
        qr_code = ImageOps.expand(
            qrcode.make(data, border=5),
            border=border,
            fill="black",
        )

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
    initial_quantity = models.IntegerField("Quantidade inicial", null=True, blank=True)
    measure_unit = models.CharField(
        "Unidade de armazenamento",
        max_length=32,
        null=True,
        blank=True,
    )
    quantity = models.IntegerField("Quantidade disponível")
    alert_below = models.IntegerField("Nível crítico")
    expiration = models.DateField("Data de validade", null=True, blank=True)
    sold_out_at = models.DateTimeField("Esgotado em", null=True, blank=True)

    available_objects = ConsumableManager()

    class Meta:
        verbose_name = "Material de consumo"
        verbose_name_plural = "Materiais de consumo"
        ordering = ["name", "-created"]

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.initial_quantity = self.quantity

        elif self.quantity <= self.alert_below:
            send_alert_email(self)

        if self.quantity == 0 and not self.sold_out_at:
            self.sold_out_at = timezone.now()

        return super().save(*args, **kwargs)

    def get_url(self):
        return reverse("update_consumable", kwargs={"pk": self.id})

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
        "Status",
        max_length=11,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    class Meta:
        verbose_name = "Material permanente"
        verbose_name_plural = "Materiais permanentes"
        ordering = ["name", "-created"]

    def get_url(self):
        return reverse("update_permanent", kwargs={"pk": self.id})
