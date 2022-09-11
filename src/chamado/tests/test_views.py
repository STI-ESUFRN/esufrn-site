from rest_framework.test import APIClient, APITestCase

from chamado.tests.helpers import sample_chamado


class TestOfferViewSetOrganizationAdmin(APITestCase):
    def setUp(self):
        self.client = APIClient()

        return super(TestOfferViewSetOrganizationAdmin, self).setUpClass()

    def some_test(self):
        sample_chamado()

        self.assertEqual(1, 1)
