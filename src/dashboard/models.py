from django.db import models

# Create your models here.


class DashboardItens(models.Model):
    name = models.CharField("Nome", max_length=100)
    link = models.CharField("Link", max_length=255)
    order = models.IntegerField(
        "Ordem", help_text="Ordem que aparecerá na barra de menu"
    )
    decoration = models.CharField(
        "Class estilo",
        blank=True,
        null=True,
        max_length=100,
        help_text="Classes CSS extra",
    )

    class Meta:
        verbose_name = "Item do menu"
        verbose_name_plural = "Itens do menu"
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.name}"


class DashboardSubItens(models.Model):
    name = models.CharField("Nome", max_length=100)
    link = models.CharField("Link", max_length=255)
    order = models.IntegerField("Ordem")
    menu = models.ForeignKey(
        DashboardItens, related_name="subitems", on_delete=models.CASCADE, null=True
    )
    decoration = models.CharField(
        "Class estilo",
        blank=True,
        null=True,
        max_length=100,
        help_text="Classes CSS extra",
    )
    aditional = models.TextField(
        "HTML Adicional", max_length=512, null=True, blank=True
    )

    class Meta:
        verbose_name = "Subitem do menu"
        verbose_name_plural = "Subitens dos menus"
        ordering = ["menu", "order"]

    def __str__(self) -> str:
        return f"{self.name}"
