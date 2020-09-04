

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from ..management.commands.createtestdata import create_test_data


class ExportTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.client.force_login(self.admin)
        self.url = reverse('admin:testapp_modela_changelist')

    def test_01_load_changelist(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
