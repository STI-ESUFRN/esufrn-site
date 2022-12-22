from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel


class Material(TimeStampedModel, SoftDeletableModel):
    class Type(models.TextChoices):
        DURABLE = "D", "Durável"
        CONSUMABLE = "C", "Consumível"

    name = models.CharField("Nome", max_length=255)
    expiration = models.DateField("Data de validade", null=True, blank=True)
    type = models.CharField("Tipo", choices=Type.choices, max_length=1)
    quantity = models.IntegerField("Quantidade disponível")
    received_date = models.DateField("Recebido em")

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"
        ordering = ["-created"]
