

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

    def test_01_dropdown(self):
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

    def test_02_filtering(self):
        queries = (
            ('', 36),
            ('dropdown_gt3=1&dropdown_lte3__isnull=True', 3),
            ('dropdown_gt3=1&multiselect_dropdown__in=3', 3),
            ('dropdown_gt3=1&multiselect_dropdown__in=3,4,5', 6),
            ('choices_dropdown__exact=3&multiselect_dropdown__in=0,1,2', 2),
            ('multiselect_dropdown__in=0,1,2&related_dropdown__id__exact=6', 1),
            ('related_dropdown__id__exact=6&multiselect_dropdown__in=3,4,5', 0),
            ('multiselect_dropdown__in=3,4,5&multiselect_related__id__in=35,34,33,32', 3),
            ('multiselect_dropdown__in=3,4,5&multiselect_related_dropdown__id__in=29,30,31,32,33,34,35', 4),
            ('boolean_annotation__exact=1&multiselect__in=0,2,4', 14),
        )
        for query, count in queries:
            resp = self.client.get(self.url + '?' + query)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('{} selected'.format(count), resp.content.decode('utf8'))
