

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

    def get_selected_by_ul_num(self, ul_num):
        xpath = '//*[@id="changelist-filter"]/ul[{}]/li[@class="selected"]'.format(ul_num)
        return self.selenium.find_elements_by_xpath(xpath)

    def click_multiselect_link(self, ul_num, li_num, item_count, selected_count, url_query):
        link = '//*[@id="changelist-filter"]/ul[{}]/li[{}]/a'.format(ul_num, li_num)
        self.selenium.find_element_by_xpath(link).click()
        self.selenium.refresh()
        self.assertEqual(self.get_item_count(), item_count)
        self.assertIn(url_query, self.get_url_query())
        self.assertEqual(len(self.get_selected_by_ul_num(ul_num)), selected_count)

    def test_01_filter(self):
        self.selenium.get(self.live_server_url + self.url_path)

        # Check the dropdown filter: changing the select input should trigger a reload.
        item_count = 9
        option_text = '2'
        url_query = 'dropdown_gt3=2'
        dropdown_gt3 = Select(self.selenium.find_element_by_id('dropdown-gt3_filter_select'))
        dropdown_gt3.select_by_visible_text(option_text)
        self.selenium.refresh()
        dropdown_gt3 = Select(self.selenium.find_element_by_id('dropdown-gt3_filter_select'))
        self.assertEqual(self.get_item_count(), item_count)
        self.assertEqual(dropdown_gt3.first_selected_option.text, option_text)
        self.assertEqual(self.get_url_query(), url_query)

        # Check the simple multiselect filter
        # (the dropdown_gt3 filter is still effectual)
        self.click_multiselect_link(3, 6, 2, 1, 'multiselect__in=4')
        self.click_multiselect_link(3, 5, 3, 2, 'multiselect__in=4,3')
        self.click_multiselect_link(3, 4, 5, 3, 'multiselect__in=4,3,2')
        self.click_multiselect_link(3, 5, 4, 2, 'multiselect__in=4,2')
        self.click_multiselect_link(3, 1, 9, 1, '')
        self.assertNotIn('multiselect__in', self.get_url_query())
