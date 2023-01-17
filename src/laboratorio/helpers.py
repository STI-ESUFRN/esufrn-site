from django.contrib.auth.models import User
from django.template.loader import render_to_string

from core.helpers import send_mail_async


def send_alert_email(material, *args, **kwargs):
    subject = (
        f"Material em nível crítico {material.name}: Restam apenas {material.quantity}"
    )
    message = f"""
        Você está recebendo este email pois um dos materiais cadastrados em nosso
        sistema acaba de entrar um nível determinado crítico.<br/><br/>
        Seguem abaixo as informações completas sobre o material.</br>
        </br>
        Nome:
        <b> {material.name}</b>;
        </br>
        Marca:
        <b> {material.brand if material.brand else "Não especificado"}</b>;
        </br>
        Data de validade:
        <b> {material.expiration if material.expiration else "Não especificado"}</b>;
        </br>
        Quantidade em estoque:
        <b> {material.quantity}</b>;
        </br>
        Quantidade de referência:
        <b> {material.reference}</b>;
        </br>
        Quantidade crítica:
        <b> {material.alert_below}</b>;
        </br>
        Descrição:
        <b> {material.description}</b>;
        </br>
        Recebido em:
        <b> {material.received_at if material.received_at else "Não especificado"}</b>;
        </br>
        Localizado em:
        <b> {material.location if material.location else "Não especificado"}</b>.</br>
        </br>
        Observações:</br>
            {material.comments}
    """

    context = {"message": message}
    msg = render_to_string("base.email_conversation.html", context)

    responsibles = User.objects.filter(groups__name="laboratorio")
    recipient_list = [recipient.user.email for recipient in responsibles]
    send_mail_async(
        subject=subject,
        recipient_list=recipient_list,
        html_message=msg,
    )
