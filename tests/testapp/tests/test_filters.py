

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from ..management.commands.createtestdata import create_test_data


class FilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.client.force_login(self.admin)
        self.url = reverse('admin:testapp_modela_changelist')

    def test_01_dropdown_select(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

        # the dropdown widget should have been loaded for dropdown_gt3
        self.assertIn('dropdown-gt3_filter_select', resp.content.decode('utf8'))
        # but not for dropdown_lte3
        self.assertNotIn('dropdown-lte3_filter_select', resp.content.decode('utf8'))

        # check other dropdown widgets
        self.assertIn('multiselect-dropdown_select', resp.content.decode('utf8'))
        self.assertIn('choices-dropdown_filter_select', resp.content.decode('utf8'))
        self.assertIn('related-dropdown_filter_select', resp.content.decode('utf8'))
        self.assertIn('multiselect-related-dropdown_select', resp.content.decode('utf8'))
