from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from core.helpers import send_mail_async
from reserva.models import Reserve, UserClassroom


def notify_admin(reserve: Reserve):
    subject = "Reserva de {}: {}".format(
        reserve.classroom.get_type_name().lower(), reserve.classroom
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
        reserve.classroom,
        reserve.date,
        reserve.event,
        reserve.shift,
        reserve.equipment,
        reserve.requester,
        reserve.email,
        reserve.phone,
    )

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
    subject = "Reserva de {}: {}".format(
        reserve.classroom.get_type_name().lower(), reserve.classroom
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
        reserve.classroom,
        reserve.date,
        reserve.event,
        reserve.shift,
        reserve.equipment,
        reserve.requester,
    )

    context = {"message": message}
    msg = render_to_string("base.email_conversation.html", context)
    send_mail_async(
        subject=subject,
        recipient_list=[reserve.email],
        html_message=msg,
    )


def notify_done(reserve: Reserve):
    title = "Reserva de {}".format(reserve.classroom)
    message = (
        "Senhor(a) {}, sua solicitação de reserva para <b>{}</b> no dia {} de {}"
        " ({}) foi <b>{}</b>. {}".format(
            reserve.requester.split()[0],
            reserve.classroom,
            reserve.date.strftime("%d"),
            _(reserve.date.strftime("%B")),
            reserve.get_shift_name().lower(),
            "aprovada" if reserve.status == "A" else "rejeitada",
            ""
            if reserve.status == "A"
            else (
                "Por favor, entre em contato com a Secretaria da Direção de Ensino"
                " a fim de viabilizarmos um possível acordo ou troca de reservas."
            ),
        )
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
