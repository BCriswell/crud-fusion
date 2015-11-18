from django.test import RequestFactory

from test_plus.test import TestCase

from . import views
from .models import Customer


class BaseCustomerTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.customer = Customer.objects.get_or_create(
                                            firstname='Testy',
                                            lastname='McTesterson',
                                            date_of_birth='1999-12-12',
                                            zip_code='30303')
        self.factory = RequestFactory()


class CustomerViewTests(BaseCustomerTestCase):

    def test_auth(self):
        self.assertLoginRequired('customers:create')
        self.assertLoginRequired('customers:list')
        self.assertLoginRequired('customers:detail', pk=self.customer[0].pk)
        self.assertLoginRequired('customers:delete', pk=self.customer[0].pk)
        self.assertLoginRequired('customers:update', pk=self.customer[0].pk)

    def test_detail_response(self):
        url = self.reverse('customers:detail', pk=self.customer[0].pk)
        with self.login(self.user):
            self.get(url)
            self.response_200()

    def test_list_response(self):
        url = self.reverse('customers:list')
        with self.login(self.user):
            self.get(url)
            self.response_200()
