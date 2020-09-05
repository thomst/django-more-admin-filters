

from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select

from ..management.commands.createtestdata import create_test_data


class LiveFilterTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        options = Options()
        options.headless = True
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        create_test_data()
        self.admin = User.objects.get(username='admin')
        self.client.force_login(self.admin)
        self.url_path = reverse('admin:testapp_modela_changelist')

        # login to selenium - using a cookie from the django test client
        admin = User.objects.get(username='admin')
        self.client.force_login(admin)
        cookie = self.client.cookies['sessionid']
        self.selenium.get(self.live_server_url + '/admin/')  #selenium will set cookie domain based on current page domain
        self.selenium.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.selenium.refresh() #need to update page for logged in user

    def get_item_count(self):
        return len(self.selenium.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))

    def get_url_query(self):
        return self.selenium.current_url.split('?')[-1].replace('%2C', ',')

    def get_selected_list_items(self, ul_num):
        xpath = '//*[@id="changelist-filter"]/ul[{}]/li[@class="selected"]'.format(ul_num)
        return self.selenium.find_elements_by_xpath(xpath)

    def use_dropdown_filter(self, select_id, option, url_query, item_count):
        select = Select(self.selenium.find_element_by_id(select_id))
        select.select_by_visible_text(option)
        self.selenium.refresh()
        select = Select(self.selenium.find_element_by_id(select_id))
        self.assertEqual(self.get_item_count(), item_count)
        self.assertEqual(self.get_url_query(), url_query)
        self.assertEqual(select.first_selected_option.text, option)

    def test_01_dropdown_filter(self):
        self.selenium.get(self.live_server_url + self.url_path)

        # Check the simple dropdown filter:
        select_id = 'dropdown-gt3_filter_select'
        url_query = 'dropdown_gt3=2'
        self.use_dropdown_filter(select_id, '2', url_query, 9)
        self.use_dropdown_filter(select_id, 'All', '', 36)

        # Check the choices dropdown filter:
        select_id = 'choices-dropdown_filter_select'
        url_query = 'choices_dropdown__exact=3'
        self.use_dropdown_filter(select_id, 'three', url_query, 4)
        self.use_dropdown_filter(select_id, 'All', '', 36)

        # # Check the related dropdown filter:
        select_id = 'related-dropdown_filter_select'
        url_query = 'related_dropdown__id__exact=9'
        self.use_dropdown_filter(select_id, 'ModelB 9', url_query, 1)
        self.use_dropdown_filter(select_id, 'All', '', 36)

    def use_multiselect_link(self, ul_num, li_num, item_count, selected_count, url_query):
        link = '//*[@id="changelist-filter"]/ul[{}]/li[{}]/a'.format(ul_num, li_num)
        self.selenium.find_element_by_xpath(link).click()
        self.selenium.refresh()
        self.assertEqual(self.get_item_count(), item_count)
        self.assertIn(url_query, self.get_url_query())
        self.assertEqual(len(self.get_selected_list_items(ul_num)), selected_count)

    def test_02_multiselect_filter(self):
        # test with activated dropdown_gt3 filter
        self.selenium.get(self.live_server_url + self.url_path + '?dropdown_gt3=2')

        # Check the simple multiselect filter
        self.use_multiselect_link(3, 6, 2, 1, 'multiselect__in=4')
        self.use_multiselect_link(3, 5, 3, 2, 'multiselect__in=4,3')
        self.use_multiselect_link(3, 4, 5, 3, 'multiselect__in=4,3,2')
        self.use_multiselect_link(3, 5, 4, 2, 'multiselect__in=4,2')
        self.use_multiselect_link(3, 1, 9, 1, '')
        self.assertNotIn('multiselect__in', self.get_url_query())

        # check the multiselect related filter
        self.use_multiselect_link(7, 35, 1, 1, 'multiselect_related__id__in=34')
        self.use_multiselect_link(7, 31, 2, 2, 'multiselect_related__id__in=34,30')
        self.use_multiselect_link(7, 27, 3, 3, 'multiselect_related__id__in=34,30,26')
        self.use_multiselect_link(7, 26, 3, 4, 'multiselect_related__id__in=34,30,26,25')
        self.use_multiselect_link(7, 35, 2, 3, 'multiselect_related__id__in=30,26,25')
        self.use_multiselect_link(7, 1, 9, 1, '')
        self.assertNotIn('multiselect_related__id__in', self.get_url_query())

    def use_multiselect_dropdown_filter(self, field, options, url_param, count):
        select = Select(self.selenium.find_element_by_id(field + '_select'))
        for value in options:
            select.select_by_value(value)
        self.selenium.find_element_by_id(field + '_submit').click()
        self.selenium.refresh()
        select = Select(self.selenium.find_element_by_id(field + '_select'))
        self.assertIn(url_param + '=' + ','.join(options), self.get_url_query())
        self.assertEqual(len(select.all_selected_options), len(options))
        self.assertEqual(self.get_item_count(), count)
        select.deselect_all()

    def test_03_multiselect_dropdown_filter(self):
        self.selenium.get(self.live_server_url + self.url_path)

        # check multiselect-dropdown
        field = 'multiselect-dropdown'
        url_param = 'multiselect_dropdown__in'
        options = [str(i) for i in range(2, 5)]
        self.use_multiselect_dropdown_filter(field, options, url_param, 18)

        # check multiselect-related-dropdown
        # (multiselect-dropdown filter is still effectual)
        field = 'multiselect-related-dropdown'
        url_param = 'multiselect_related_dropdown__id__in'
        options = [str(i) for i in range(1, 9)]
        self.use_multiselect_dropdown_filter(field, options, url_param, 4)
