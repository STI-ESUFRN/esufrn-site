from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _

from core.helpers import send_mail_async
from reserva.enums import Shift, Status
from reserva.models import Reserve, UserClassroom


def notify_admin(reserve: Reserve):
    subject = f"Reserva de {reserve.classroom}"
    message = f"""
        Uma solicitação de reserva de sala foi realizada.
        Por favor realizar a validação.<br/>
        Sala: {reserve.classroom}<br/>
        Data: {reserve.date}<br/>
        Evento: {reserve.event}<br/>
        Turno: {reserve.shift}<br/>
        Equipamento/Software: {reserve.equipment}<br/>
        Solicitante: {reserve.requester}<br/>
        Email do solicitante: {reserve.email}<br/>
        Telefone: {reserve.phone}
    """

    context = {"message": message}
    msg = render_to_string("base.email_conversation.html", context)

    responsibles = UserClassroom.objects.filter(classroom=reserve.classroom)
    recipient_list = [recipient.user.email for recipient in responsibles]

    send_mail_async(
        subject=subject,
        recipient_list=recipient_list,
        html_message=msg,
    )


def notify_requester(reserve: Reserve):
    subject = f"Reserva de {reserve.classroom}"

    uri = reverse("cancel_reserve", kwargs={"uuid": reserve.uuid})
    cancel_url = f"{settings.HOST_URL}{uri}"

    message = f"""
        Solicitação de reserva de sala feita com sucesso. Aguarde a validação.<br/>
        <hr/>
        <b>Detalhes:</b><br/>
        Sala: {reserve.classroom}<br/>
        Data: {reserve.date}<br/>
        Evento: {reserve.event}<br/>
        Turno: {Shift(reserve.shift).label}<br/>
        Equipamento/Software: {reserve.equipment}<br/>
        Solicitante: {reserve.requester}<br/>
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


def notify_done(reserve: Reserve):
    rejected_message = (
        "Por favor, entre em contato com a Secretaria da Direção de Ensino a fim de"
        " viabilizarmos um possível acordo ou troca de reservas."
    )
    done_status = {Status.APPROVED, Status.CANCELED}
    title = f"Reserva de {reserve.classroom}"
    message = (
        f"Senhor(a) {reserve.requester.split()[0]}, sua solicitação de reserva para"
        f" <b>{reserve.classroom}</b> no dia {reserve.date.strftime('%d')} de"
        f" {_(reserve.date.strftime('%B'))} ({Shift(reserve.shift).label}) foi"
        f" <b>{Status(reserve.status).label}</b>."
        f" {'' if reserve.status in done_status else rejected_message}"
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
