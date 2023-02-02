from django.db import models
from django.forms import ValidationError


class Itens(models.Model):
    name = models.CharField("Nome", max_length=100)
    TYPE_CHOICES = (("hover", "Hover"), ("link", "Link"))
    action_type = models.CharField(
        "Tipo",
        max_length=100,
        choices=TYPE_CHOICES,
        default="hover",
        help_text=(
            "Hover: Ao clicar ou passar o mouse sobre, abrirá os subitens; Link: Ao"
            " clicar abrirá o link inserido."
        ),
    )
    footer = models.BooleanField(
        "Rodapé",
        help_text="Mostrar menu e seus respectivos subitens no rodapé da página",
        default=False,
    )
    link = models.CharField(
        "Link", max_length=255, blank=True, help_text="Usar apenas se o tipo for Link"
    )
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

    def get_link(self):
        if self.action_type == "link" and self.link:
            return self.link
        else:
            return "-"

    get_link.short_description = "Link"

    def clean(self):
        if self.action_type == "link" and not self.link:
            raise ValidationError(
                "Este tipo de menu requer que seja especificado um link"
            )

    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu nível 1"
        verbose_name_plural = "Menu nível 1"
        ordering = ["order", "name"]


class SubItens(models.Model):
    name = models.CharField("Nome", max_length=100)
    link = models.CharField("Link", max_length=255)
    order = models.IntegerField("Ordem")
    menu = models.ForeignKey(
        Itens, related_name="subitems", on_delete=models.CASCADE, null=True
    )
    decoration = models.CharField(
        "Class estilo",
        blank=True,
        null=True,
        max_length=100,
        help_text="Classes CSS extra",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Menu nível 2"
        verbose_name_plural = "Menu nível 2"
        ordering = ["menu", "order", "name"]
