from datetime import datetime

from django.db import models
from django.forms import ValidationError
from reserva.models import Classroom

# Create your models here.


class Patrimonio(models.Model):

    model = models.CharField(verbose_name="Modelo", max_length=64)
    dmp = models.CharField(verbose_name="Tombamento",
                           max_length=64, null=True, blank=True)

    TIPO_CHOICES = (
        ("C", "Computador de mesa"),
        ("N", "Notebook"),
        ("D", "Projetor"),
        ("P", "Periférico"),
        ("E", "Cabo"),
        ("O", "Outro"),
    )
    category = models.CharField(verbose_name="Tipo",
                                max_length=1, choices=TIPO_CHOICES)

    def get_category(self):
        for index, e in self.TIPO_CHOICES:
            if self.category == index:
                return e

    STATUS_CHOICES = (
        ("D", "Disponível"),
        ("E", "Emprestado"),
    )
    status = models.CharField(verbose_name="Status",
                              max_length=1, choices=STATUS_CHOICES, default='D')

    last_updated = models.DateTimeField(
        verbose_name="Última atualização", auto_now=True)

    def clean(self):
        if self.status == "E" and PatrimonioEmprestimo.objects.filter(patrimony=self, loan__return_date__isnull=True):
            raise ValidationError(
                "Não é possível emprestar {}: patrimônio já foi emprestado".format(self))

    def save(self, *args, **kwargs):
        self.clean()

        super(Patrimonio, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.model, self.dmp)


class Maquina(models.Model):

    patrimony = models.ForeignKey(
        Patrimonio, verbose_name="Patrimônio", on_delete=models.CASCADE)

    ram = models.IntegerField(
        verbose_name="RAM", null=True, blank=True)
    hdd = models.IntegerField(
        verbose_name="HDD", null=True, blank=True)

    STATUS_CHOICES = (
        ("R", "Reserva"),
        ("G", "Bom"),
        ("W", "Atenção"),
        ("B", "Ruim"),
    )
    status = models.CharField(verbose_name="Status",
                              max_length=1, choices=STATUS_CHOICES)

    obs = models.TextField(verbose_name="Observações",
                           max_length=1000, null=True, blank=True)

    def get_dmp(self):
        return self.patrimony.dmp

    get_dmp.short_description = "Tombamento"

    def get_model(self):
        return self.patrimony.model

    get_model.short_description = "Modelo"

    class Meta:
        verbose_name = "Máquina"
        verbose_name_plural = "Máquinas"
        ordering = ["patrimony__model", "patrimony__dmp"]

    def __str__(self):
        return self.patrimony.model


class Emprestimo(models.Model):
    name = models.CharField(verbose_name="Solicitante", max_length=100)
    contact = models.CharField(
        verbose_name="Contato", max_length=100, null=True)
    obs = models.TextField(verbose_name="Contato",
                           max_length=1000, null=True, blank=True)

    classroom = models.ForeignKey(
        Classroom, verbose_name="Sala", on_delete=models.CASCADE, null=True, blank=True)
    borrow_date = models.DateTimeField(verbose_name="Data de empréstimo")
    return_date = models.DateTimeField(
        verbose_name="Recebido em", null=True, blank=True)
    STATUS_CHOICES = (
        ("A", "Aguardando devolução"),
        ("D", "Devolvido"),
        ("C", "Cancelado"),
    )
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="A")

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        self.clean()

        if self.status == "A":
            self.return_date = None
        elif self.status == "D":
            self.return_date = datetime.now()

        super(Emprestimo, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.save()


class PatrimonioEmprestimo(models.Model):
    patrimony = models.ForeignKey(
        Patrimonio, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Quantidade", default=1)
    loan = models.ForeignKey(Emprestimo, on_delete=models.CASCADE)

    def clean(self):
        if self.loan.return_date:
            self.patrimony.status = "D"
        else:
            self.patrimony.status = "E"

        self.patrimony.save()

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"
        ordering = ["patrimony__model"]
