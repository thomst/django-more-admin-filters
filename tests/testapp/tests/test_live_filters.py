
import time

from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select

from ..management.commands.createtestdata import create_test_data


class FilterPage:
    WAIT_FOR_RELOAD = 1
    URL_PATH = reverse('admin:testapp_modela_changelist')

    # ul-indexes
    MULTISELECT_UL = 3
    MULTISELECT_RELATED_UL = 7

    def __init__(self, selenium, base_url):
        self.base_url = base_url
        self.url = base_url + self.URL_PATH
        self.selenium = selenium
        self.current_url = self.selenium.current_url

    def login(self, client):
        # login to selenium - using a cookie from the django test client
        admin = User.objects.get(username='admin')
        client.force_login(admin)
        cookie = client.cookies['sessionid']
        #selenium will set cookie domain based on current page domain
        self.selenium.get(self.base_url + '/admin/')
        self.selenium.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        #need to update page for logged in user
        self.selenium.refresh()

    def get(self, url_query=str()):
        return self.selenium.get(self.url + '?' + url_query)

    def wait_for_reload(self):
        now = time.time()
        while self.current_url == self.selenium.current_url:
            self.selenium.refresh()
            if time.time() - now < self.WAIT_FOR_RELOAD:
                msg = "Could not reload live server page. Waited {} sec."
                raise RuntimeError(msg.format(self.WAIT_FOR_RELOAD))
        else:
            self.current_url = self.selenium.current_url
            return True

    @property
    def item_count(self):
        return len(self.selenium.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))

    @property
    def url_query(self):
        return self.selenium.current_url.split('?')[-1].replace('%2C', ',')

    def get_selected_li_count(self, ul):
        return len(ul.find_elements_by_css_selector('li.selected'))

    def use_dropdown_filter(self, select_id, option):
        select = Select(self.selenium.find_element_by_id(select_id))
        select.select_by_visible_text(option)
        self.wait_for_reload()
        return Select(self.selenium.find_element_by_id(select_id))

    def use_multiselect_filter(self, ul_num, title):
        uls_css = '#changelist-filter ul'
        a_xpath = f'li/a[text() = "{title}"]'
        ul = self.selenium.find_elements_by_css_selector(uls_css)[ul_num-1]
        ul.find_element_by_xpath(a_xpath).click()
        self.wait_for_reload()
        return self.selenium.find_elements_by_css_selector(uls_css)[ul_num-1]

    def use_multiselect_dropdown_filter(self, field, options):
        select = Select(self.selenium.find_element_by_id(field + '_select'))
        for value in options:
            select.select_by_value(value)
        self.selenium.find_element_by_id(field + '_submit').click()
        self.wait_for_reload()
        return Select(self.selenium.find_element_by_id(field + '_select'))


class LiveFilterTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        cls.selenium = WebDriver(options=options)
        cls.url_path = reverse('admin:testapp_modela_changelist')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        create_test_data()
        self.page = FilterPage(self.selenium, self.live_server_url)
        self.page.login(self.client)

    def check_dropdown_filter(self, select_id, query_key, query_value, option, count):
        select = self.page.use_dropdown_filter(select_id, option)
        self.assertEqual(self.page.item_count, count)
        self.assertEqual(select.first_selected_option.text, option)
        if option == 'All':
            self.assertNotIn(query_key, self.page.url_query)
        else:
            self.assertIn(query_key + query_value, self.page.url_query)

    def test_01_dropdown_filter(self):
        self.page.get()

        # check simple dropdown filter
        select_id, query_key = 'dropdown-gt3_filter_select', 'dropdown_gt3='
        self.check_dropdown_filter(select_id, query_key, '2', '2', 9)
        self.check_dropdown_filter(select_id, query_key, '', 'All', 36)

       # Check choices dropdown filter:
        select_id, query_key = 'choices-dropdown_filter_select', 'choices_dropdown__exact='
        self.check_dropdown_filter(select_id, query_key, '3', 'three', 4)
        self.check_dropdown_filter(select_id, query_key, '', 'All', 36)

        # Check related dropdown filter:
        select_id, query_key = 'related-dropdown_filter_select', 'related_dropdown__id__exact='
        self.check_dropdown_filter(select_id, query_key, '9', 'ModelB 9', 1)
        self.check_dropdown_filter(select_id, query_key, '', 'All', 36)

    def check_multiselect_filter(self, ul_num, query_key, query_value, option, count, selected):
        ul = self.page.use_multiselect_filter(ul_num, option)
        self.assertEqual(self.page.item_count, count)
        self.assertEqual(self.page.get_selected_li_count(ul), selected)
        if option == 'All':
            self.assertNotIn(query_key, self.page.url_query)
        else:
            self.assertIn(query_key + query_value, self.page.url_query)

    def test_02_multiselect_filter(self):
        # start with an already filtered changelist
        self.page.get('dropdown_gt3=2')

        # check simple multiselect filter
        ul_num, query_key = self.page.MULTISELECT_UL, 'multiselect__in='
        self.check_multiselect_filter(ul_num, query_key, '4', '4', 2, 1)
        self.check_multiselect_filter(ul_num, query_key, '4,3', '3', 3, 2)
        self.check_multiselect_filter(ul_num, query_key, '4,3,2', '2', 5, 3)
        self.check_multiselect_filter(ul_num, query_key, '', 'All', 9, 1)

        # check the multiselect related filter
        ul_num, query_key = self.page.MULTISELECT_RELATED_UL, 'multiselect_related__id__in='
        self.check_multiselect_filter(ul_num, query_key, '34', 'ModelB 34', 1, 1)
        self.check_multiselect_filter(ul_num, query_key, '34,30', 'ModelB 30', 2, 2)
        self.check_multiselect_filter(ul_num, query_key, '34,30,26', 'ModelB 26', 3, 3)
        self.check_multiselect_filter(ul_num, query_key, '30,26', 'ModelB 34', 2, 2)
        self.check_multiselect_filter(ul_num, query_key, '', 'All', 9, 1)

    def check_multiselect_dropdown_filter(self, field, options, query_key, count):
        select = self.page.use_multiselect_dropdown_filter(field, options)
        self.assertEqual(len(select.all_selected_options), len(options))
        self.assertEqual(self.page.item_count, count)
        self.assertIn(query_key + ','.join(options), self.page.url_query)
        select.deselect_all()

    def test_03_multiselect_dropdown_filter(self):
        self.page.get()

        # check multiselect-dropdown
        field, query_key = 'multiselect-dropdown', 'multiselect_dropdown__in='
        options = [str(i) for i in range(2, 5)]
        self.check_multiselect_dropdown_filter(field, options, query_key, 18)

        # check multiselect-related-dropdown
        # (multiselect-dropdown filter is still effectual)
        field, query_key = 'multiselect-related-dropdown', 'multiselect_related_dropdown__id__in='
        options = [str(i) for i in range(1, 9)]
        self.check_multiselect_dropdown_filter(field, options, query_key, 4)
