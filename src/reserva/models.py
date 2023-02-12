from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from model_utils.models import SoftDeletableModel, TimeStampedModel
from multiselectfield import MultiSelectField
from rest_framework.exceptions import ValidationError

from reserva.enums import Shift, Status
from reserva.managers import PeriodManager, ReserveManager


class Classroom(models.Model):
    class Type(models.TextChoices):
        CLASSROOM = "sal", "Sala de aula"
        LABORATORY = "lab", "Laboratório"
        AUDITORIUM = "aud", "Auditório"

    class Floor(models.TextChoices):
        GROUND = "0", "Térreo"
        ST_FLOOR = "1", "1º Andar"

    name = models.CharField("Nome da sala", max_length=64, blank=True, null=True)
    acronym = models.CharField("Acrônimo", null=True, blank=True, max_length=16)

    type = models.CharField("Tipo de sala", max_length=3, choices=Type.choices)
    number = models.CharField("Número da sala", max_length=10)

    days_required = models.IntegerField(
        verbose_name="Prazo mínimo de reserva", default=1
    )
    justification_required = models.BooleanField(
        "Requer justificativa de uso", default=False
    )

    floor = models.CharField(
        "Andar", max_length=25, choices=Floor.choices, default=Floor.GROUND
    )

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        ordering = ["floor", "number"]

    @property
    def full_name(self):
        if self.name:
            return f"{self.name} - {self.number}"

        return f"{self.Type(self.type).label} - {self.number}"

    def __str__(self):
        return self.full_name

    def clean(self):
        if self.acronym and not self.name:
            raise ValidationError(
                {
                    "name": [
                        "Caso informada um acrônimo, por favor informar também o nome"
                        " da sala."
                    ]
                }
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class UserClassroom(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Responsável",
        related_name="classrooms",
        on_delete=models.CASCADE,
    )
    classroom = models.ForeignKey(
        Classroom,
        verbose_name="Sala",
        related_name="responsible",
        on_delete=models.CASCADE,
    )

    def get_user_email(self):
        return self.user.email

    get_user_email.short_description = "Email do responsável"

    def clean(self):
        if not self.user.email:
            raise ValidationError(
                {"user": ["O responsável precisa ter um email associado a ele."]}
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"
        unique_together = ["user", "classroom"]


class Reserve(TimeStampedModel, SoftDeletableModel):
    classroom = models.ForeignKey(
        Classroom,
        verbose_name="Sala de aula",
        on_delete=models.CASCADE,
    )
    event = models.CharField("Evento", max_length=100)
    requester = models.CharField("Nome do solicitante", max_length=100)
    date = models.DateField("Data para a reserva")
    shift = models.CharField("Turno", choices=Shift.choices, max_length=1)
    email = models.EmailField("E-mail", max_length=100)
    phone = models.CharField("Telefone", max_length=16, null=True, blank=True)
    cause = models.TextField("Justificativa", max_length=512, null=True, blank=True)
    equipment = models.CharField(
        "Equipamento multimídia", max_length=200, null=True, blank=True
    )
    status = models.CharField(
        "Estado da reserva",
        choices=Status.choices,
        default=Status.WAITING,
        max_length=1,
    )
    obs = models.TextField("Observação", max_length=1000, null=True, blank=True)
    email_response = models.TextField("Resposta", null=True, blank=True)
    declare = models.BooleanField(
        "Supervisionado por docente",
        default=False,
        help_text=(
            "Marcando esta caixa, você declara que a sala contará com a supervisão de"
            " um docente no momento da aula."
        ),
    )
    admin_created = models.BooleanField(
        verbose_name="Criado pela administração", default=False
    )

    objects = ReserveManager()

    def __str__(self):
        return str(self.classroom)

    class Meta:
        verbose_name = "Reserva pontual"
        verbose_name_plural = "Reservas pontuais"
        ordering = ["created"]


class Period(TimeStampedModel, SoftDeletableModel):
    class Course(models.TextChoices):
        ESU01 = "ESU01", "Técnico em Enfermagem"
        ESU02 = "ESU02", "Técnico em Registros e Informações em Saúde"
        ESU06 = "ESU06", "Técnico em Vigilância em Saúde"
        ESU05 = "ESU05", "Técnico em Agente Comunitário de Saúde"
        ESU07 = "ESU07", "Técnico em Massoterapia"
        ESU10 = "ESU10", "Graduação Tecnológica em Gestão Hospitalar"
        MPPSE = "MPPSE", "Mestrado Profissional"
        ENF = "ENF", "Outros"

    class Weekdays(models.TextChoices):
        MONDAY = "1", _("Monday")
        TUESDAY = "2", _("Tuesday")
        WEDNESDAY = "3", _("Wednesday")
        THURSDAY = "4", _("Thursday")
        FRIDAY = "5", _("Friday")
        SATURDAY = "6", _("Saturday")
        SUNDAY = "7", _("Sunday")

    classroom = models.ForeignKey(
        Classroom,
        verbose_name="Sala de aula",
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        "Estado da reserva",
        choices=Status.choices,
        default=Status.WAITING,
        max_length=1,
    )

    date_begin = models.DateField("Início do período")
    date_end = models.DateField("Fim do período")

    workload = models.IntegerField("Carga horária", null=True)

    weekdays = MultiSelectField("Dias da semana", choices=Weekdays.choices)

    classname = models.CharField("Nome da turma", max_length=100)
    classcode = models.CharField("Código do componente", max_length=16)

    course = models.CharField("Nome do curso", choices=Course.choices, max_length=8)

    period = models.CharField("Período letivo", max_length=8)
    class_period = models.CharField("Turma", max_length=8)

    shift = MultiSelectField("Turno", choices=Shift.choices)

    requester = models.CharField("Nome completo", max_length=100)
    email = models.EmailField("E-mail", max_length=100)
    phone = models.CharField("Telefone", max_length=16)

    equipment = models.CharField(
        "Equipamento multimídia",
        max_length=200,
        null=True,
        blank=True,
        help_text=(
            "Informe se preciso, algum equipamento ou software adicional necessário"
            " para as aulas."
        ),
    )

    obs = models.TextField("Observação", max_length=1000, null=True, blank=True)

    objects = PeriodManager()

    @property
    def event(self):
        return f"{self.classcode} - {self.classname}"

    def __str__(self):
        if self.classcode:
            return f"{self.classcode}: {self.classname}"
        else:
            return self.classname

    class Meta:
        verbose_name = "Reserva de período"
        verbose_name_plural = "Reservas de período"
        ordering = [
            "-period",
            "-class_period",
            "course",
            "date_begin",
            "date_end",
            "classname",
        ]

    def get_short_weekdays(self):
        days = {
            "1": "2ª",
            "2": "3ª",
            "3": "4ª",
            "4": "5ª",
            "5": "6ª",
            "6": "7",
            "7": "8",
        }
        return ", ".join([days[day] for day in self.weekdays])

    def get_saturdays(self):
        return self.days.filter(date__iso_week_day=6).values("date").distinct().count()

    def get_total_days(self):
        return self.days.values("date").distinct().count()


class ReserveDay(models.Model):
    reserve = models.ForeignKey(
        Reserve, related_name="days", on_delete=models.CASCADE, null=True
    )
    period = models.ForeignKey(
        Period, related_name="days", on_delete=models.CASCADE, null=True
    )

    date = models.DateField("Data da reserva")
    shift = models.CharField(choices=Shift.choices, max_length=1)

    classroom = models.ForeignKey(
        Classroom,
        related_name="reserves",
        on_delete=models.CASCADE,
    )

    active = models.BooleanField("Ativo", default=True)

    @property
    def status(self):
        return (self.reserve or self.period).status

    @property
    def event(self):
        return (self.reserve or self.period).event

    def clean(self):
        if self.status == Status.APPROVED and self.active:
            reserves = ReserveDay.objects.filter(
                Q(period__status=Status.APPROVED) | Q(reserve__status=Status.APPROVED),
                date=self.date,
                classroom=self.classroom,
                shift=self.shift,
                active=True,
            )
            if self.reserve:
                reserves = reserves.exclude(reserve=self.reserve)
            if self.period:
                reserves = reserves.exclude(period=self.period)

            if reserves:
                raise ValidationError(
                    {
                        "date": [
                            "Já existe uma reserva aprovada para o dia"
                            f" {self.date.strftime('%d-%m-%Y')}"
                        ]
                    }
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Dia da reserva"
        verbose_name_plural = "Dias da reserva"
        ordering = ["date", "shift"]
