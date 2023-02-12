from django.db import models


class Shift(models.TextChoices):
    MORNING = ("M", "Manhã")
    AFTERNOON = ("T", "Tarde")
    NIGHT = ("N", "Noite")


class Status(models.TextChoices):
    WAITING = ("E", "Esperando")
    CANCELED = ("C", "Cancelada")
    REJECTED = ("R", "Rejeitada")
    APPROVED = ("A", "Aprovada")
    DONE = ("D", "Concluída")
