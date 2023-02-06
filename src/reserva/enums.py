from django.db import models


class Shift(models.TextChoices):
    MORNING = ("M", "Manhã")
    AFTERNOON = ("T", "Tarde")
    NIGHT = ("N", "Noite")


class Status(models.TextChoices):
    WAITING = ("E", "Esperando")
    CANCELED = ("C", "Cancelado")
    REJECTED = ("R", "Rejeitado")
    APPROVED = ("A", "Aprovado")
    DONE = ("D", "Concluído")
