from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from principal.helpers import emailToken
from principal.tests.helpers import sample_news, sample_newsletter, sample_page


class PrincipalViewsTest(APITestCase):
    def test_home_view(self):
        sample_news(_quantity=10)
        url = reverse("principal:home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagina_view(self):
        page = sample_page()
        url = reverse("principal:pagina", kwargs={"path": page.path})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_equipe_view(self):
        url = reverse("principal:equipe")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_docuementos_view(self):
        url = reverse("principal:documentos")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ensino_sobre_view(self):
        url = reverse("principal:ensino_sobre")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ensino_tecnico_view(self):
        url = reverse("principal:ensino_tecnico")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ensino_graduacao_view(self):
        url = reverse("principal:ensino_graduacao")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ensino_especializacao_view(self):
        url = reverse("principal:ensino_especializacao")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ensino_mestrado_view(self):
        url = reverse("principal:ensino_mestrado")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_ensino_pronatec_view(self):
        url = reverse("principal:ensino_pronatec")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_publicacoes_outras_view(self):
        url = reverse("principal:publicacoes_outras")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_busca_view(self):
        url = reverse("principal:busca")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_noticia_view(self):
        news = sample_news()
        url = reverse("principal:noticia", kwargs={"slug": news.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_noticias_view(self):
        url = reverse("principal:noticias")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsubscribe_view(self):
        newsletter = sample_newsletter(consent=True)
        token = emailToken(newsletter.email)
        url = reverse("principal:unsubscribe")
        response = self.client.get(url, {"token": token, "email": newsletter.email})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_subscribe_view(self):
    #     url = reverse("principal:subscribe")
    #     payload = {
    #         "name_person": "sample person",
    #         "email": "sample@mail.com",
    #         "consent": "true",
    #         "category": "editais,turmas,outras",
    #     }
    #     response = self.client.generic(
    #         method="POST",
    #         path=url,
    #         data=json.dumps(payload),
    #         content_type="application/json",
    #     )

    #     newsletter = Newsletter.objects.get(email=payload["email"])
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(newsletter.category, payload["category"])
