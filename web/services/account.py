from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from web.models import Wallet

class AccountService(object):

    @classmethod
    @transaction.atomic
    def CreateAccount(cls, username, password):
        try:
            user = User.objects.create_user(username=username,
                                            password=password)
        except IntegrityError:
            return False, 'Username already exist'
        
        wallet = Wallet.objects.create(user=user,
                                       currency='EUR')

        return True, wallet
