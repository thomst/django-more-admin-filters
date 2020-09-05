

from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

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

    def test_01_filter(self):
        self.selenium.get(self.live_server_url + self.url_path)
