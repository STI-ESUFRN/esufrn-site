from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone

from core.helpers import send_email_with_attachments, send_mail_async
from django.core.mail import send_mail
from eventos.models import Event
from principal.helpers import paginator


def evento(request, slug):
    try:
        event = Event.available_objects.get(slug=slug)

        context = {
            "event": event,
            "crumbs": [
                {"name": "Eventos"},
                {"name": event.name},
            ],
        }

        return render(request, "eventos.evento.html", context)

    except Event.DoesNotExist as e:
        raise Http404 from e


def eventos(request):
    today = timezone.now().date()

    events = Event.available_objects.all()

    category = request.GET.get("category")
    if category == "concluido":
        events = events.filter(date_end__lt=today)
    elif category == "andamento":
        events = events.filter(date_begin__lte=today, date_end__gte=today)
    elif category == "agendado":
        events = events.filter(date_begin__gt=today)

    period = request.GET.get("period")
    if period:
        if period == "hora":
            delta = timedelta(hours=1)
        elif period == "dia":
            delta = timedelta(days=1)
        elif period == "semana":
            delta = timedelta(weeks=1)
        elif period == "mes":
            delta = relativedelta(months=+1)
        elif period == "ano":
            delta = relativedelta(years=+1)
        else:
            delta = timedelta()

        now = timezone.now()
        events = events.filter(created__range=(now - delta, now))

    page = int(request.GET.get("page", "1"))
    result_obj, qnt, intervalo = paginator(page, events)

    context = {
        "events": events,
        "crumbs": [
            {"name": "Eventos"},
        ],
        "categories": {
            "parameter": "category=",
            "options": [
                {
                    "verbose_name": "Tudo",
                    "verbose_name_plural": "Tudo",
                    "query": "",
                },
                {
                    "verbose_name": "Concluído",
                    "verbose_name_plural": "Concluídos",
                    "query": "concluido",
                },
                {
                    "verbose_name": "Em andamento",
                    "verbose_name_plural": "Em andamento",
                    "query": "andamento",
                },
                {
                    "verbose_name": "Agendado",
                    "verbose_name_plural": "Agendados",
                    "query": "agendado",
                },
            ],
        },
        "result_obj": result_obj,
        "qnt": qnt,
        "intervalo": intervalo,
    }

    return render(request, "eventos.eventos.html", context)


def eventos_concluidos(request):
    events = Event.available_objects.filter(date_end__lt=timezone.now().date())

    page = int(request.GET.get("page", "1"))
    result_obj, qnt, intervalo = paginator(page, events)

    context = {
        "events": events,
        "crumbs": [
            {"name": "Eventos"},
            {"name": "Concluído"},
        ],
        "result_obj": result_obj,
        "qnt": qnt,
        "intervalo": intervalo,
    }

    return render(request, "eventos.eventos.html", context)


def submissao_trabalhos(request):
    return render(request, "eventos.submissao_trabalhos.html", {})


def submeter_trabalho(request):
    if request.method != "POST":
        return redirect("submissao_trabalhos")

    try:
        # Extrair dados do formulário
        data = request.POST.get("data", {})
        
        # Dados do artigo
        titulo = request.POST.get("data[Artigo][nome]", "")
        area_tematica_id = request.POST.get("data[Artigo][area_tematica_id]", "")
        modalidade_id = request.POST.get("data[Artigo][modalidade_id]", "")
        palavras_chave = request.POST.get("data[Artigo][palavras_chave]", "")
        resumo = request.POST.get("data[Artigo][resumo]", "")
        apresentador = request.POST.get("data[Artigo][apresentador]", "")
        
        # Determinar tipo de submissão
        tipo_submissao = "Resumo Simples" if area_tematica_id == "54999" else "Resumo Expandido"
        
        # Determinar modalidade
        modalidade = "Oral" if modalidade_id == "1" else "Pôster" if modalidade_id == "2" else "Não informada"
        
        # Arquivos
        arquivo_sem_autor = request.FILES.get("data[Artigo][arquivo]")
        arquivo_com_autor = request.FILES.get("data[Artigo][segundo_arquivo]")
        
        # Coletar autores
        autores = []
        i = 1
        while True:
            nome = request.POST.get(f"data[Autor][{i}][name]")
            email = request.POST.get(f"data[Autor][{i}][email]")
            if not nome and not email:
                break
            autores.append({"nome": nome, "email": email})
            i += 1
        
        # Montar mensagem do email para administração
        autores_html = "<br/>".join([f"{idx + 1}. {autor['nome']} ({autor['email']})" for idx, autor in enumerate(autores)])
        
        # Informação sobre anexos
        anexos_info = ""
        if arquivo_sem_autor:
            anexos_info += f"<li>Trabalho SEM nome dos autores: {arquivo_sem_autor.name}</li>"
        if arquivo_com_autor:
            anexos_info += f"<li>Trabalho COM nome dos autores: {arquivo_com_autor.name}</li>"
        
        if anexos_info:
            anexos_info = f"<h3>Arquivos Anexados:</h3><ul>{anexos_info}</ul><hr/>"
        
        message_admin = f"""
        <h2>Nova Submissão de Trabalho</h2>
        <hr/>
        <p><strong>Tipo de Submissão:</strong> {tipo_submissao}</p>
        <p><strong>Título do Trabalho:</strong> {titulo}</p>
        <p><strong>Modalidade de Apresentação:</strong> {modalidade}</p>
        <p><strong>Palavras-chave:</strong> {palavras_chave}</p>
        <p><strong>Apresentador:</strong> {apresentador}</p>
        <hr/>
        <h3>Resumo:</h3>
        <p style="white-space: pre-wrap;">{resumo}</p>
        <hr/>
        <h3>Autores:</h3>
        <p>{autores_html}</p>
        <hr/>
        {anexos_info}
        """
        
        context_admin = {"message": message_admin}
        msg_admin = render_to_string("base.email_conversation.html", context_admin)
        
        # Email de destino da administração
        recipient_email = "suporte@es.ufrn.br"
        
        # Preparar anexos para o email da administração
        attachments = []
        if arquivo_sem_autor:
            attachments.append(arquivo_sem_autor)
        if arquivo_com_autor:
            attachments.append(arquivo_com_autor)
        
        # Enviar email para administração com anexos
        subject_admin = f"[Submissão de Trabalho] {tipo_submissao} - {titulo}"
        
        send_email_with_attachments(
            subject=subject_admin,
            html_message=msg_admin,
            recipient_list=[recipient_email],
            attachments=attachments if attachments else None,
        )
        
        # Enviar email de confirmação para o autor principal
        if autores and autores[0].get("email"):
            autor_principal_nome = autores[0].get("nome", "")
            autor_principal_email = autores[0].get("email")
            
            message_author = f"""
            <h2>Confirmação de Submissão de Trabalho</h2>
            <hr/>
            <p>Olá, <strong>{autor_principal_nome}</strong>!</p>
            <p>Sua submissão de trabalho foi recebida com sucesso. Segue abaixo os detalhes:</p>
            <hr/>
            <p><strong>Tipo de Submissão:</strong> {tipo_submissao}</p>
            <p><strong>Título do Trabalho:</strong> {titulo}</p>
            <p><strong>Modalidade de Apresentação:</strong> {modalidade}</p>
            <p><strong>Palavras-chave:</strong> {palavras_chave}</p>
            <p><strong>Apresentador:</strong> {apresentador}</p>
            <hr/>
            <h3>Autores:</h3>
            <p>{autores_html}</p>
            <hr/>
            <p>Em breve você receberá um retorno sobre a avaliação do seu trabalho.</p>
            <p>Atenciosamente,<br/>Equipe de Organização</p>
            """
            
            context_author = {"message": message_author}
            msg_author = render_to_string("base.email_conversation.html", context_author)
            
            send_mail_async(
                subject=f"Confirmação de Submissão - {titulo}",
                recipient_list=[autor_principal_email],
                html_message=msg_author,
            )
        
        messages.success(request, "Trabalho submetido com sucesso! Você receberá um email de confirmação em breve.")
        
    except Exception as e:
        messages.error(request, f"Erro ao submeter trabalho: {str(e)}")
    
    return redirect("submissao_trabalhos")


def inscricao(request):
    context = {
        "crumbs": [
            {"name": "Eventos"},
            {"name": "Inscrição"},
        ],
    }
    return render(request, "eventos.inscricao.html", context)


def submeter_inscricao(request):
    if request.method != "POST":
        return redirect("inscricao")

    try:
        # --- 1. Extração e Validação ---
        nome_aluno = request.POST.get("nome_aluno", "").strip()
        cpf_matricula = request.POST.get("cpf_matricula", "").strip()
        email_aluno = request.POST.get("email_aluno", "").strip()
        
        if not nome_aluno or not cpf_matricula or not email_aluno:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")
            return redirect("inscricao")
        
        # --- 2. Preparação do Email Admin ---
        message_admin = f"""
        <h2>Nova Inscrição em Evento</h2>
        <hr/>
        <p><strong>Nome do Aluno:</strong> {nome_aluno}</p>
        <p><strong>CPF ou Matrícula:</strong> {cpf_matricula}</p>
        <p><strong>E-mail:</strong> {email_aluno}</p>
        <hr/>
        <p><small>Data da inscrição: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}</small></p>
        """
        
        context_admin = {"message": message_admin}
        msg_admin = render_to_string("base.email_conversation.html", context_admin)
        recipient_email = "suporte@es.ufrn.br"
        
        # --- 3. Envio Síncrono Admin (Debug Ativado) ---
        print(f"Tentando enviar email Admin para {recipient_email}...") # Log no terminal
        send_mail(
            subject=f"[Inscrição em Evento] {nome_aluno}",
            message="",  # Fallback de texto puro obrigatório
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            html_message=msg_admin,
            fail_silently=False, # Importante: False para mostrar o erro se falhar
        )
        
        # --- 4. Preparação do Email Aluno ---
        message_aluno = f"""
        <h2>Confirmação de Inscrição</h2>
        <hr/>
        <p>Olá, <strong>{nome_aluno}</strong>!</p>
        <p>Sua inscrição foi recebida com sucesso! Segue abaixo os dados informados:</p>
        <hr/>
        <p><strong>Nome:</strong> {nome_aluno}</p>
        <p><strong>CPF ou Matrícula:</strong> {cpf_matricula}</p>
        <p><strong>E-mail:</strong> {email_aluno}</p>
        <hr/>
        <p>Em breve você receberá mais informações sobre o evento.</p>
        <p>Atenciosamente,<br/>Equipe de Organização</p>
        """
        
        context_aluno = {"message": message_aluno}
        msg_aluno = render_to_string("base.email_conversation.html", context_aluno)
        
        # --- 5. Envio Síncrono Aluno ---
        print(f"Tentando enviar email Aluno para {email_aluno}...") # Log no terminal
        send_mail(
            subject="Confirmação de Inscrição - Evento ESUFRN",
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email_aluno],
            html_message=msg_aluno,
            fail_silently=False,
        )
        
        # Sucesso
        messages.success(request, "Inscrição realizada com sucesso! Você receberá um email de confirmação em breve.")
        
    except Exception as e:
        # Log detalhado do erro no console do servidor
        print(f"ERRO CRÍTICO NO ENVIO DE EMAIL: {e}")
        # Mensagem para o usuário (pode ser genérica em produção, mas aqui ajuda a debugar)
        messages.error(request, f"Erro ao processar inscrição (Email): {str(e)}")
    
    return redirect("inscricao")