from django.contrib.auth.models import User
from django.test import TestCase

from web.services.account import AccountService


class AccountServiceCase(TestCase):
    
    fixtures = ['user.yaml']

    def test_create_account(self):
        self.assertTrue(AccountService.CreateAccount('test2', 'test2'))
        self.assertEquals('test2', User.objects.get(username='test2').username)

    def test_create_account_with_already_used_username(self):
        status, _ = AccountService.CreateAccount('test', 'test')
        self.assertFalse(status)
