import threading
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField


class Classroom(models.Model):
    name = models.CharField("Nome da sala", max_length=64, blank=True, null=True)
    acronym = models.CharField("Acrônimo", null=True, blank=True, max_length=16)
    TIPO_CHOICES = (
        ("sal", "Sala de aula"),
        ("lab", "Laboratório"),
        ("aud", "Auditório"),
    )
    type = models.CharField("Tipo de sala", max_length=3, choices=TIPO_CHOICES)
    number = models.CharField("Número da sala", max_length=10)

    days_required = models.IntegerField(
        verbose_name="Prazo mínimo de reserva", default=1
    )
    justification_required = models.BooleanField(
        "Requer justificativa de uso", default=False
    )

    FLOOR_CHOICES = (
        ("0", "Térreo"),
        ("1", "1º Andar"),
        # ("2", "2º Andar"),
    )
    floor = models.CharField("Andar", max_length=25, choices=FLOOR_CHOICES, default="0")

    def __str__(self):
        return self.get_classroom_name()

    def get_classroom_name(self):
        if self.name:
            return self.name + " - " + str(self.number)

        return self.get_type_name() + " - " + str(self.number)

    def get_floor_name(self):
        for index, row in self.FLOOR_CHOICES:
            if index == self.floor:
                return row

    def get_type_name(self):
        for index, row in self.TIPO_CHOICES:
            if index == self.type:
                return row

    def clean(self):
        if self.acronym and not self.name:
            raise ValidationError(
                "Caso informada um acrônimo, por favor informar também o nome da sala."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super(Classroom, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        ordering = ["floor", "number"]


class UserClassroom(models.Model):
    user = models.ForeignKey(User, verbose_name="Responsável", on_delete=models.CASCADE)
    classroom = models.ForeignKey(
        Classroom, verbose_name="Sala", on_delete=models.CASCADE
    )

    def get_user_email(self):
        return self.user.email

    get_user_email.short_description = "Email do responsável"

    def clean(self):
        if not self.user.email:
            raise ValidationError("O responsável precisa ter um email associado a ele.")

        if UserClassroom.objects.filter(
            user=self.user, classroom=self.classroom
        ).exclude(id=self.id):
            raise ValidationError("Esta entrada já existe.")

    def save(self, *args, **kwargs):
        self.clean()

        super(UserClassroom, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"


class Reserve(models.Model):
    classroom = models.ForeignKey(
        Classroom,
        verbose_name="Sala de aula",
        related_name="reserves",
        on_delete=models.CASCADE,
    )
    date = models.DateField("Data para a reserva")
    created_at = models.DateTimeField("Data do pedido", auto_now_add=True)
    refresh_at = models.DateTimeField("Data de atualização do pedido", auto_now=True)
    event = models.CharField("Evento", max_length=100, null=True)

    SHIFT_CHOICES = (("M", "Manhã"), ("T", "Tarde"), ("N", "Noite"))
    shift = models.CharField("Turno", choices=SHIFT_CHOICES, default="M", max_length=1)
    cause = models.TextField("Justificativa", max_length=512, null=True, blank=True)
    equipment = models.CharField(
        "Equipamento multimídia", max_length=200, null=True, blank=True
    )
    requester = models.CharField("Nome do solicitante", max_length=100)
    email = models.EmailField("E-mail", max_length=100)
    phone = models.CharField("Telefone", max_length=16, null=True, blank=True)

    STATUS_CHOICES = (("A", "Aprovado"), ("R", "Rejeitado"), ("E", "Esperando"))
    status = models.CharField(
        "Estado da reserva", choices=STATUS_CHOICES, default="E", max_length=1
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

    def __str__(self):
        return str(self.classroom)

    def get_shift_name(self):
        for index, row in self.SHIFT_CHOICES:
            if index == self.shift:
                return row

    def get_status_name(self):
        for index, row in self.STATUS_CHOICES:
            if index == self.status:
                return row

    def clean_form(self):
        if not self.pk:
            if self.classroom.type == "lab" and not self.declare:
                raise ValidationError(
                    "Este tipo de sala requer que o usuário declare que esteja presente"
                    " um docente no momento da aula."
                )

            if self.classroom.justification_required and not self.cause:
                raise ValidationError(
                    "Este tipo de sala requer que o usuário informe uma justificativa"
                    " para seu uso."
                )

            if self.shift == "M":
                time = "12:30"
            elif self.shift == "T":
                time = "18:30"
            else:
                time = "22:15"

            date = datetime.strptime("{} {}".format(self.date, time), "%Y-%m-%d %H:%M")
            now = datetime.today()

            diff = (date - now).days
            if diff < 0:
                raise ValidationError(
                    "Você não pode reservar uma sala para uma data passada."
                )

            if diff < self.classroom.days_required:
                raise ValidationError(
                    "Você não pode reservar esta sala para a data informada: A reserva"
                    " para esta sala requer antecedência de {} dia{}.".format(
                        self.classroom.days_required,
                        "s" if self.classroom.days_required > 1 else "",
                    )
                )

    def clean(self):
        if self.status == "A":
            reserves = Reserve.objects.filter(
                date=self.date,
                status="A",
                classroom=self.classroom,
                shift=self.shift,
            ).exclude(id=self.id)
            periodreserves = PeriodReserveDay.objects.filter(
                date=self.date,
                period__status="A",
                period__classroom=self.classroom,
                shift=self.shift,
            ).exclude(active=False)

            if reserves or periodreserves:
                raise ValidationError(
                    "Já existe uma reserva aprovada para o dia {} - {}{}".format(
                        self.date.strftime("%d/%m/%Y"),
                        self.get_shift_name(),
                        "."
                        if self.admin_created
                        else (
                            ". Por favor, entre em contato com a secretaria a fim de"
                            " viabilizarmos outro dia para esta reserva."
                        ),
                    )
                )

    def save(self, *args, **kwargs):
        pk = self.pk

        if not self.admin_created:
            self.clean_form()
        self.clean()

        super(Reserve, self).save(*args, **kwargs)

        if pk is None:
            self.notify_admin()
            self.notify_requester()

    def update(self, **kwargs):
        self.__dict__.update(kwargs)
        self.save()

    def notify_admin(self):
        subject = "Reserva de {}: {}".format(
            self.classroom.get_type_name().lower(), self.classroom
        )
        message = """
            Uma solicitação de reserva de sala foi realizada.
            Por favor realizar a validação.<br/>
            Sala: {0}<br/>
            Data: {1}<br/>
            Evento: {2}<br/>
            Turno: {3}<br/>
            Equipamento/Software: {4}<br/>
            Solicitante: {5}<br/>
            Email do solicitante: {6}<br/>
            Telefone: {7}
        """.format(
            self.classroom,
            self.date,
            self.event,
            self.shift,
            self.equipment,
            self.requester,
            self.email,
            self.phone,
        )

        context = {"message": message}
        msg = render_to_string("base.email_conversation.html", context)

        recipients = UserClassroom.objects.filter(classroom=self.classroom)
        recipient_list = []
        for recipient in recipients:
            recipient_list.append(recipient.user.email)

        threading.Thread(
            target=send_mail,
            args=(
                (
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    recipient_list,
                    False,
                    None,
                    None,
                    None,
                    msg,
                )
            ),
        ).start()

    def notify_requester(self):
        subject = "Reserva de {}: {}".format(
            self.classroom.get_type_name().lower(), self.classroom
        )
        message = """
            Solicitação de reserva de sala feita com sucesso. Aguarde a validação.<br/>
            Sala: {0}<br/>
            Data: {1}<br/>
            Evento: {2}<br/>
            Turno: {3}<br/>
            Equipamento/Software: {4}<br/>
            Solicitante: {5}
        """.format(
            self.classroom,
            self.date,
            self.event,
            self.shift,
            self.equipment,
            self.requester,
        )

        context = {"message": message}
        msg = render_to_string("base.email_conversation.html", context)
        threading.Thread(
            target=send_mail,
            args=(
                (
                    subject,
                    "",
                    settings.EMAIL_HOST_USER,
                    [self.email],
                    False,
                    None,
                    None,
                    None,
                    msg,
                )
            ),
        ).start()

    def notify(self):
        title = "Reserva de {}".format(self.classroom)
        message = (
            "Senhor(a) {}, sua solicitação de reserva para <b>{}</b> no dia {} de {}"
            " ({}) foi <b>{}</b>. {}".format(
                self.requester.split()[0],
                self.classroom,
                self.date.strftime("%d"),
                _(self.date.strftime("%B")),
                self.get_shift_name().lower(),
                "aprovada" if self.status == "A" else "rejeitada",
                ""
                if self.status == "A"
                else (
                    "Por favor, entre em contato com a Secretaria da Direção de Ensino"
                    " a fim de viabilizarmos um possível acordo ou troca de reservas."
                ),
            )
        )
        context = {
            "message": message,
            "opitional": self.email_response,
        }
        msg = render_to_string("base.email_conversation.html", context)
        threading.Thread(
            target=send_mail,
            args=(
                (
                    title,
                    "",
                    settings.EMAIL_HOST_USER,
                    [self.email],
                    False,
                    None,
                    None,
                    None,
                    msg,
                )
            ),
        ).start()

    class Meta:
        verbose_name = "Reserva pontual"
        verbose_name_plural = "Reservas pontuais"
        ordering = ["-created_at"]


class PeriodReserve(models.Model):
    STATUS_CHOICES = (("A", "Aprovado"), ("R", "Rejeitado"), ("E", "Esperando"))

    classroom = models.ForeignKey(
        Classroom,
        verbose_name="Sala de aula",
        related_name="period_reserves",
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        "Estado da reserva", choices=STATUS_CHOICES, default="E", max_length=1
    )

    date_begin = models.DateField("Início do período")
    date_end = models.DateField("Fim do período")

    workload = models.IntegerField("Carga horária", null=True)

    NUMERIC_DAYS_OF_THE_WEEK = {
        ("1", "2ª"),
        ("2", "3ª"),
        ("3", "4ª"),
        ("4", "5ª"),
        ("5", "6ª"),
        ("6", "7"),
        ("7", "1"),
    }
    DAYS_OF_THE_WEEK = {
        ("1", _("Monday")),
        ("2", _("Tuesday")),
        ("3", _("Wednesday")),
        ("4", _("Thursday")),
        ("5", _("Friday")),
        ("6", _("Saturday")),
        ("7", _("Sunday")),
    }
    weekdays = MultiSelectField(
        "Dias da semana", choices=sorted(DAYS_OF_THE_WEEK), max_length=14
    )

    created_at = models.DateTimeField("Data da reserva", auto_now_add=True)
    refresh_at = models.DateTimeField("Data de atualização da reserva", auto_now=True)

    classname = models.CharField("Nome da turma", max_length=100)
    classcode = models.CharField("Código do componente", max_length=16, null=True)
    COURSE_CHOICES = (
        ("ESU01", "Técnico em Enfermagem"),
        ("ESU02", "Técnico em Registros e Informações em Saúde"),
        ("ESU06", "Técnico em Vigilância em Saúde"),
        ("ESU05", "Técnico em Agente Comunitário de Saúde"),
        ("ESU07", "Técnico em Massoterapia"),
        ("ESU10", "Graduação Tecnológica em Gestão Hospitalar"),
        ("MPPSE", "Mestrado Profissional"),
        ("ENF", "Outros"),
    )
    course = models.CharField(
        "Nome do curso", choices=COURSE_CHOICES, max_length=8, null=True
    )

    period = models.CharField("Período letivo", max_length=8, default="2022.2")
    class_period = models.CharField(
        "Turma",
        max_length=8,
        default="2021.2",
        help_text="Ano de ingresso. Ex: 2020.2, 2021.6",
    )

    SHIFT_CHOICES = (("M", "Manhã"), ("T", "Tarde"), ("N", "Noite"))

    shift = MultiSelectField(
        "Turno", choices=SHIFT_CHOICES, max_length=len(SHIFT_CHOICES) * 2
    )

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

    def get_courses():
        courses = []
        for index, row in PeriodReserve.COURSE_CHOICES:
            courses.append((index, row))

        return courses

    def get_course_name(self):
        for index, row in self.COURSE_CHOICES:
            if index == self.course:
                return row

    def get_weekdays(self):
        list = []
        for index, row in sorted(self.DAYS_OF_THE_WEEK):
            if index in self.weekdays:
                list.append(row)
        return list

    def get_numeric_weekdays(self):
        list = []
        for index, row in sorted(self.NUMERIC_DAYS_OF_THE_WEEK):
            if index in self.weekdays:
                list.append(row)
        return list

    def get_days(self):
        return (
            PeriodReserveDay.objects.order_by("date")
            .filter(period=self)
            .values_list("date", flat=True)
            .distinct()
        )

    def get_saturdays(self):
        return (
            PeriodReserveDay.objects.order_by("date")
            .filter(period=self, date__iso_week_day=6)
            .values_list("date", flat=True)
            .distinct()
        )

    def __str__(self):
        if self.classcode:
            return "{}: {}".format(self.classcode, self.classname)
        else:
            return self.classname

    def check_days(self):
        reserves = Reserve.objects.filter(
            date__range=(self.date_begin, self.date_end),
            date__iso_week_day__in=self.weekdays,
            status="A",
            classroom=self.classroom,
            shift__in=self.shift,
        )

        period_reserves = PeriodReserveDay.objects.filter(
            date__range=(self.date_begin, self.date_end),
            date__iso_week_day__in=self.weekdays,
            period__status="A",
            period__classroom=self.classroom,
            shift__in=self.shift,
            active=True,
        ).exclude(period=self)

        if self.pk:
            for reserve in reserves:
                day = PeriodReserveDay.objects.filter(
                    period=self, date=reserve.date
                ).first()
                if day and not day.active:
                    reserves = reserves.exclude(id=reserve.id)

            for reserve in period_reserves:
                day = PeriodReserveDay.objects.filter(
                    period=self, date=reserve.date
                ).first()
                if day and not day.active:
                    reserves = reserves.exclude(id=reserve.id)

        if reserves or period_reserves:
            dates = ""
            for i in reserves:
                dates += "{} - {}, ".format(i.date.strftime("%d/%m/%Y"), i.shift)
            for i in period_reserves:
                dates += "{} - {}, ".format(i.date.strftime("%d/%m/%Y"), i.shift)

            raise ValidationError(
                "Já existe uma reserva aprovada para o{0} dia{0}: ".format(
                    "s" if len(reserves) + len(period_reserves) > 1 else ""
                )
                + dates.rstrip(", ")
            )

    def create_days(self):
        if self.status == "A":
            self.check_days()

        reserve_days = PeriodReserveDay.objects.filter(period=self)
        if reserve_days:
            reserve_days.delete()

        start_date = self.date_begin
        end_date = self.date_end
        delta = timedelta(days=1)
        while start_date <= end_date:
            if start_date.isoweekday() in self.weekdays:
                for shift in self.shift:
                    PeriodReserveDay.objects.create(
                        period=self, date=start_date, shift=shift
                    )
            start_date += delta

    def save(self, *args, **kwargs):
        weekdays = []
        for i in self.weekdays:
            weekdays.append(int(i))
        self.weekdays = weekdays

        if self.status == "A":
            self.check_days()

        super(PeriodReserve, self).save(*args, **kwargs)
        self.create_days()

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

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


class PeriodReserveDay(models.Model):
    period = models.ForeignKey(
        PeriodReserve, verbose_name="Período", on_delete=models.CASCADE
    )
    date = models.DateField("Data da reserva")
    active = models.BooleanField("Ativo", default=True)
    SHIFT_CHOICES = (("M", "Manhã"), ("T", "Tarde"), ("N", "Noite"))
    shift = models.CharField(
        verbose_name="Turno", choices=SHIFT_CHOICES, max_length=1, default="M"
    )

    def get_shift_name(self):
        for index, row in self.SHIFT_CHOICES:
            if index == self.shift:
                return row

    def __str__(self):
        return (
            str(self.period.classroom)
            + " no dia "
            + self.date.strftime("%d/%m/%Y")
            + " - "
            + self.shift
        )

    def get_period_classroom(self):
        return str(self.period.classroom)

    get_period_classroom.short_description = "Sala"

    def get_period_requester(self):
        return self.period.requester

    get_period_requester.short_description = "Professor"

    def clean(self):
        if self.period.status == "A" and self.active:
            reserves = Reserve.objects.filter(
                date=self.date,
                status="A",
                classroom=self.period.classroom,
                shift=self.shift,
            )
            periodreserves = (
                PeriodReserveDay.objects.filter(
                    date=self.date,
                    period__status="A",
                    period__classroom=self.period.classroom,
                    shift=self.shift,
                )
                .exclude(period=self.period)
                .exclude(active=False)
            )

            if reserves or periodreserves:
                raise ValidationError(
                    "Já existe uma reserva aprovada para o dia {}".format(
                        self.date.strftime("%d-%m-%Y")
                    )
                )

    def save(self, **kwargs):
        self.clean()
        super(PeriodReserveDay, self).save(**kwargs)

    def update(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        self.save()

    class Meta:
        verbose_name = "Dia da reserva"
        verbose_name_plural = "Dias da reserva"
        ordering = ["date", "shift"]


class MaterialReservation(models.Model):
    pass
