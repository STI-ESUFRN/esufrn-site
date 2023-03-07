from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.tests.helpers import sample_group, sample_user
from reserva.tests.helpers import sample_period


class PeriodViewGroupReserva(TestCase):
    def setUp(self) -> None:
        self.user = sample_user(
            username="user",
            password="password",
            groups=[
                sample_group(name="reserva"),
            ],
        )

        self.client.login(username="user", password="password")

    def test_periodo_home_view(self):
        url = reverse("periodo_home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_period_history_view(self):
        url = reverse("period_history")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_period_view(self):
        url = reverse("create_period")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_periods_view(self):
        url = reverse("list_periods")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_period_view(self):
        period = sample_period()
        url = reverse("update_period", kwargs={"pk": period.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PeriodViewGroupSuporte(TestCase):
    def setUp(self) -> None:
        self.user = sample_user(
            username="user",
            password="password",
            groups=[
                sample_group(name="suporte"),
            ],
        )

        self.client.login(username="user", password="password")

    def test_periodo_home_view(self):
        url = reverse("periodo_home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_period_history_view(self):
        url = reverse("period_history")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_period_view(self):
        url = reverse("create_period")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_periods_view(self):
        url = reverse("list_periods")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_period_view(self):
        period = sample_period()
        url = reverse("update_period", kwargs={"pk": period.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PeriodViewAnnonimousUser(TestCase):
    def test_periodo_home_view(self):
        url = reverse("periodo_home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_period_history_view(self):
        url = reverse("period_history")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_create_period_view(self):
        url = reverse("create_period")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_list_periods_view(self):
        url = reverse("list_periods")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_update_period_view(self):
        period = sample_period()
        url = reverse("update_period", kwargs={"pk": period.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
