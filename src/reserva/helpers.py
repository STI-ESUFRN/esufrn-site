from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _

from core.helpers import send_mail_async
from reserva.enums import Shift, Status


def notify_admin(reserve):
    subject = f"Reserva de {reserve.classroom}"
    message = f"""
        Uma solicitação de reserva de sala foi realizada.
        Favor verificar o sistema.<br/>
        <hr/>
        Sala: <b>{reserve.classroom}</b><br/>
        Data: <b>{reserve.date.strftime("%d/%n/%Y")}</b><br/>
        Evento: <b>{reserve.event}</b><br/>
        Turno: <b>{Shift(reserve.shift).label}</b><br/>
        Equipamento/Software: <b>{reserve.equipment or "Não"}</b><br/>
        Solicitante: <b>{reserve.requester}</b><br/>
        Email do solicitante: <b>{reserve.email}</b><br/>
        Telefone: <b>{reserve.phone}</b>
    """

    context = {"message": message}
    msg = render_to_string("base.email_conversation.html", context)

    responsibles = reserve.classroom.responsible.all()
    recipient_list = [recipient.user.email for recipient in responsibles]

    send_mail_async(
        subject=subject,
        recipient_list=recipient_list,
        html_message=msg,
    )


def notify_requester(reserve):
    subject = f"Reserva de {reserve.classroom}"

    uri = reverse("cancel_reserve", kwargs={"uuid": reserve.uuid})
    cancel_url = f"{settings.HOST_URL}{uri}"

    message = f"""
        Solicitação de reserva de sala feita com sucesso. Você deverá ser notificado da
        mudança do status da sua reserva em breve.<br/>
        <hr/>
        Sala: <b>{reserve.classroom}</b><br/>
        Data: <b>{reserve.date}</b><br/>
        Evento: <b>{reserve.event}</b><br/>
        Turno: <b>{Shift(reserve.shift).label}</b><br/>
        Equipamento/Software: <b>{reserve.equipment or "Não"}</b><br/>
        Solicitante: <b>{reserve.requester}</b><br/>
        <hr/>
        <p>
            Enviou algum dado errado? Cancele sua reserva a qualquer momento clicando
            <a href="{cancel_url}">aqui</a>
        </p>

    """

    context = {"message": message}
    msg = render_to_string("base.email_conversation.html", context)

    send_mail_async(
        subject=subject,
        recipient_list=[reserve.email],
        html_message=msg,
    )


def notify_done(reserve):
    rejected_message = (
        "Por favor, entre em contato com a Secretaria da Direção de Ensino a fim de"
        " viabilizarmos um possível acordo ou troca de reservas."
    )

    title = f"Reserva de {reserve.classroom}"
    message = (
        f"Senhor(a) {reserve.requester.split()[0]}, sua solicitação de reserva para"
        f" <b>{reserve.classroom}</b> no dia {reserve.date.strftime('%d')} de"
        f" {_(reserve.date.strftime('%B'))} ({Shift(reserve.shift).label}) foi"
        f" <b>{Status(reserve.status).label}</b>."
        f" {rejected_message if reserve.status == Status.REJECTED else ''}"
    )
    context = {
        "message": message,
        "opitional": reserve.email_response,
    }
    msg = render_to_string("base.email_conversation.html", context)

    send_mail_async(
        subject=title,
        recipient_list=[reserve.email],
        html_message=msg,
    )
