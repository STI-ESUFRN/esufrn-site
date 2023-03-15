from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.tests.helpers import sample_group, sample_user


class ReserveViewGroupReserva(TestCase):
    def setUp(self) -> None:
        self.user = sample_user(
            username="user",
            password="password",
            groups=[
                sample_group(name="reserva"),
            ],
        )

        self.client.login(username="user", password="password")

    def test_reserve_home_view(self):
        url = reverse("reserve_home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reserve_history_view(self):
        url = reverse("reserve_history")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_reserve_view(self):
        url = reverse("create_reserve")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reserve_report_view(self):
        url = reverse("reserve_report")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReserveViewGroupSuporte(TestCase):
    def setUp(self) -> None:
        self.user = sample_user(
            username="user",
            password="password",
            groups=[
                sample_group(name="suporte"),
            ],
        )

        self.client.login(username="user", password="password")

    def test_reserve_home_view(self):
        url = reverse("reserve_home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reserve_history_view(self):
        url = reverse("reserve_history")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_reserve_view(self):
        url = reverse("create_reserve")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reserve_report_view(self):
        url = reverse("reserve_report")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReserveViewAnnonimousUser(TestCase):
    def test_reserve_home_view(self):
        url = reverse("reserve_home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_reserve_history_view(self):
        url = reverse("reserve_history")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_reserve_view(self):
        url = reverse("create_reserve")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_reserve_report_view(self):
        url = reverse("reserve_report")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
