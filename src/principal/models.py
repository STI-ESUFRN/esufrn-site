import os
import threading
from datetime import datetime
from urllib.parse import unquote

from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.mail import get_connection, send_mail
from django.core.validators import EmailValidator
from django.db import models
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from multiselectfield import MultiSelectField
from PIL import Image

from esufrn.settings import MEDIA_ROOT
from principal.helpers import emailToken


class News(models.Model):
    title = models.CharField("Título da notícia", max_length=400)
    subtitle = models.CharField("Subtítulo da notícia", max_length=500)
    slug = models.SlugField(
        "Atalho",
        max_length=255,
        help_text=(
            "Este campo será preenchido automaticamente, ele representa a URL da"
            " notícia. Ele é único e nenhuma outra notícia deverá ter o mesmo atalho."
        ),
    )
    news = RichTextUploadingField("Notícia")
    isImportant = models.BooleanField(
        "Destaque?",
        default=False,
        help_text=(
            "Caso seja marcado, esse campo indica a notícia aparecerá no slide da"
            " página principal, logo abaixo do menu."
        ),
    )

    class Category(models.TextChoices):
        NEWS = "noticia", "Notícia (Newsletter - Notícias)"
        EVENT = "evento", "Evento"
        PROCESS = "processo", "Processo (Newsletter - Abertura de Turmas)"
        COURSE = "concurso", "Concurso (Newsletter - Editais de Cursos)"

    author = models.CharField("Nome do autor", max_length=50)
    category = models.CharField(
        "Categoria", max_length=8, choices=Category.choices, default=Category.NEWS
    )

    image = models.ImageField(
        upload_to="blog/imagens",
        verbose_name="Imagem da postagem",
        null=True,
        blank=True,
        help_text=(
            "Esta imagem será a capa da postagem. Ela aparecerá no topo da página da"
            " notícia, no plano de fundo do link na página principal e no plano de"
            " fundo do link no Facebook."
        ),
    )

    published_at = models.DateTimeField("Publicado em", auto_now_add=True)
    modified_at = models.DateTimeField("Modificado em", auto_now=True)

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("noticia", kwargs={"slug": self.slug})

    def send_newsletter(self):
        if self.category == "noticia":
            to_send = Newsletter.objects.filter(category__contains="outras")
            cat = "Notícias"
        elif self.category == "evento":
            to_send = Newsletter.objects.filter(category__contains="turmas")
            cat = "Turmas abertas"
        else:
            to_send = Newsletter.objects.filter(category__contains="editais")
            cat = "Editais de curso"

        context = {
            "title": self.title,
            "subtitle": self.subtitle,
            "news": strip_tags(self.news),
            "url": self.get_absolute_url(),
            "author": self.author,
            "image": self.image,
            "published_at": self.published_at,
            "modified_at": self.modified_at,
            "host_url": settings.HOST_URL,
        }

        def send():
            connection = get_connection()
            connection.open()

            subject = "Newsletter ESUFRN - {}".format(cat)
            for registration in to_send:
                email = registration.email
                context["newsletter_email"] = {
                    "email": email,
                    "token": emailToken(email),
                }

                msg_html = render_to_string("base_email.html", context)
                send_mail(
                    subject,
                    self.news,
                    settings.EMAIL_HOST_USER,
                    [email],
                    False,
                    None,
                    None,
                    connection,
                    msg_html,
                )

            connection.close()

        threading.Thread(target=send).start()

    def save(self, *args, **kwargs):
        have_id = self.pk
        super().save(*args, **kwargs)
        if self.image:
            filepath = unquote(os.path.split(MEDIA_ROOT)[0] + self.image.url)
            picture = Image.open(filepath)
            picture = picture.convert("RGB")
            picture.save(
                os.path.join(MEDIA_ROOT, self.image.name),
                "JPEG",
                optimize=True,
                quality=40,
            )

        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.published_at.date()}")

        super().save(*args, **kwargs)

        if have_id is None:
            self.send_newsletter()


class File(models.Model):
    name = models.CharField("Nome", max_length=250)
    file = models.FileField(
        upload_to="files/", verbose_name="Arquivo", null=True, max_length=255
    )

    published_at = models.DateTimeField(
        "Adicionado em", default=datetime.now, null=True
    )

    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = "Arquivos"
        ordering = ["name"]

    def __str__(self):
        return self.name


class NewsAttachment(models.Model):
    blog = models.ForeignKey(News, related_name="attachments", on_delete=models.CASCADE)
    file = models.ForeignKey(File, verbose_name="Arquivo", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
        ordering = ["blog__title"]


class Team(models.Model):
    TYPE_CHOICES = (("docente", "Docente"), ("servidor", "Servidor"))

    name = models.CharField("Nome", max_length=100)
    photo = models.ImageField(
        upload_to="equipe/imagens",
        verbose_name="Imagem da Servidor",
        default="/equipe/base/avatar.jpg",
    )
    kind = models.CharField(
        "Tipo", max_length=8, choices=TYPE_CHOICES, default="docente"
    )
    sigaa = models.URLField(max_length=300, blank=True)
    cv = models.URLField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Equipe"
        verbose_name_plural = "Equipe"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField("Nome", max_length=250, help_text="Será o título da página")
    path = models.SlugField(
        "Caminho",
        max_length=250,
        unique=True,
        help_text=(
            "Insira todo o caminho (PATH) depois de 'escoladesaude.ufrn.br/pagina/'."
            " Não insira novas '/'"
        ),
    )
    content = RichTextUploadingField("Conteúdo", config_name="page")

    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"
        ordering = ["path", "name"]

    def get_absolute_url(self):
        return reverse("pagina", kwargs={"path": self.path})

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    TYPE_CHOICES = (
        ("editais", "Editais de Cursos"),
        ("turmas", "Abertura de Turmas"),
        ("outras", "Outras Notícias"),
    )

    name_person = models.CharField("Nome", max_length=110)
    email = models.EmailField("Email", max_length=110)
    category = MultiSelectField("Tipo", max_length=21, choices=TYPE_CHOICES)

    subscribed_at = models.DateTimeField("Inscrito desde", auto_now_add=True, null=True)
    last_updated = models.DateTimeField("Última atualização", auto_now=True, null=True)

    consent = models.BooleanField(
        "Termos de uso",
        default=False,
        help_text=(
            "Ao marcar essa caixa, o usuário declara que leu e concorda com a política"
            " de privacidade da ESUFRN."
        ),
    )

    class Meta:
        verbose_name = "Newsletter"
        verbose_name_plural = "Newsletter"
        ordering = ["name_person"]

    def __str__(self):
        return self.name_person

    def clean(self):
        if not self.name_person:
            raise ValidationError("O campo de nome não pode estar vazio")
        if not self.email:
            raise ValidationError("O campo de email não pode estar vazio")
        if not self.category or self.category[0] == "":
            raise ValidationError("Escolha pelo menos uma categoria")
        if not self.consent:
            raise ValidationError("Você precisa concordar com os termos de uso")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    name = models.CharField("Nome", max_length=100)
    occupation = models.CharField("Ocupação", max_length=100)
    testimonial = models.CharField("Depoimento", max_length=100)
    file = models.FileField(
        upload_to="depoimentos/", verbose_name="Imagem", null=True, blank=True
    )

    class Meta:
        verbose_name = "Depoimento"
        verbose_name_plural = "Depoimentos"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Document(models.Model):
    name = models.CharField("Nome", max_length=250)
    authors = models.CharField(
        "Autores",
        help_text="Nome autor ou dos autores, separados por ';'",
        max_length=250,
        null=True,
        blank=True,
    )
    CATEGORY_CHOICES = (
        ("institucional", "Institucional"),
        ("ensino", "Ensino"),
        ("outros", "Outros documentos"),
        ("publicacoes", "Publicações"),
    )
    category = models.CharField(
        verbose_name="Categoria", choices=CATEGORY_CHOICES, max_length=32
    )

    TYPE_CHOICES = (("arquivo", "Arquivo"), ("link", "Link"))
    document_type = models.CharField(
        "Tipo",
        max_length=100,
        choices=TYPE_CHOICES,
        default="arquivo",
        help_text=(
            "Documento: Ao clicar, abrirá o documento em uma nova guia; Link: Ao clicar"
            " abrirá o link inserido em uma nova guia."
        ),
    )

    file = models.FileField(
        upload_to="files/documentos", verbose_name="Arquivo", max_length=255, blank=True
    )
    link = models.CharField("Link", max_length=1024, blank=True)

    date = models.DateField(
        "Data do documento", default=datetime.now, null=True, blank=True
    )

    published_at = models.DateTimeField("Publicado em", auto_now_add=True)
    modified_at = models.DateTimeField("Modificado em", auto_now=True)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ["-date", "-published_at"]

    def get_url(self):
        if self.document_type == "arquivo":
            return self.file
        if self.document_type == "link":
            return self.link

    get_url.short_description = "Caminho"

    def clean(self):
        if self.document_type == "arquivo" and not self.file.name:
            raise ValidationError(
                "O tipo do documento exige que seja escolhido um arquivo"
            )
        if self.document_type == "link" and not self.link:
            raise ValidationError(
                "O tipo do documento exige que seja informado um link"
            )

    def __str__(self):
        return self.name


class Message(models.Model):
    name = models.CharField("Nome", max_length=100)
    contact = models.CharField("Contato", max_length=100)
    message = models.CharField("Mensagem", max_length=500)

    sent_at = models.DateTimeField("Enviado em", default=datetime.now, blank=True)

    def clean(self):
        if self.name is None:
            raise ValidationError("O campo de nome não pode estar em branco")
        if self.contact is None:
            raise ValidationError("O campo de contato não pode estar em branco")
        if self.message is None:
            raise ValidationError("O campo de mensagem não pode estar em branco")

        validator = EmailValidator(message="Endereço de email inválido")
        validator(self.contact)

    def save(self, *args, **kwargs):
        pk = self.pk
        self.clean()

        super().save(*args, **kwargs)

        if not pk:
            self.notify()

    def notify(self):
        message = (
            "Alguém entrou em contato usando o formulário de contato de nosso"
            f" site.\n\nNome: {self.name}\nContato: {self.contact}\n\n  {self.message}"
        )

        threading.Thread(
            target=send_mail,
            args=(
                (
                    "Formulário do site da ESUFRN",
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.CONTACT_EMAIL],
                )
            ),
        ).start()

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ["-sent_at"]

    def __str__(self):
        return self.message


class Alert(TimeStampedModel):
    title = models.CharField("Título", max_length=100)
    content = RichTextUploadingField("Conteúdo", config_name="page")
    expires_at = models.DateTimeField("Exibir até")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        ordering = ["-created"]
