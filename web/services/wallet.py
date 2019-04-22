from decimal import Decimal
from django.db import transaction
from web.models import Wallet, WalletTransaction

class WalletService(object):

    """Service for manager user wallets transactions"""
    def __init__(self, user):
        self.wallets = Wallet.objects.filter(user=user).order_by('created')
        self.current_user = self.wallets[0].user

    def deposit(self, amount):
        self._increment_eur_wallet(amount, 'deposit')
        return True

    def bonus(self, amount, currency, wagering_requirement=False):

        if currency == "EUR":
            self._increment_eur_wallet(amount, 'eur_bonus')
        else:
            self._create_bonus_wallet(amount, currency, wagering_requirement)
        return True

    def process_bet(self, bet_wallet, amount, won=False):
        action = 'bet_won'

        if not won:
            amount = amount * -1
            action = 'bet_lose'
        
        if bet_wallet.currency == 'EUR':
            self._increment_eur_wallet(amount, action, is_bet=True)
        else:
            self._increment_bns_wallet(bet_wallet, amount, action)
        return True

    def get_next_wallet_to_bet(self, beat_amount):
        wallet = Wallet.objects.filter(user=self.current_user,
                                       amount__gte=beat_amount).order_by('created').first()
        return wallet

    @transaction.atomic
    def _increment_eur_wallet(self, amount, action, is_bet=False):
        wallet_amount = self.wallets[0].amount + Decimal(amount)
        update_values = {'amount': wallet_amount}

        if is_bet:
            update_values['bet_amount'] = self.wallets[0].bet_amount + Decimal(abs(amount))
        
        Wallet.objects.filter(pk=self.wallets[0].id).update(**update_values)

        WalletTransaction.objects.create(action=action,
                                         amount=amount,
                                         wallet=self.wallets[0])
        return True

    @transaction.atomic
    def _increment_bns_wallet(self, wallet, amount, action):
        wallet_amount = wallet.amount + Decimal(amount)
        bet_amount = wallet.bet_amount + Decimal(abs(amount))
        Wallet.objects.filter(pk=wallet.id).update(amount=wallet_amount,
                                                   bet_amount=bet_amount)

        WalletTransaction.objects.create(action=action,
                                         amount=amount,
                                         wallet=wallet)
        return True

    @transaction.atomic
    def _create_bonus_wallet(self, amount, currency, wagering_requirement):
        bonus_wallet = Wallet.objects.create(user=self.current_user,
                                             amount=amount,
                                             currency=currency,
                                             bonus_initial=amount,
                                             wagering_requirement=wagering_requirement)
        
        WalletTransaction.objects.create(action='bonus',
                                         amount=amount,
                                         wallet=bonus_wallet)
        return True
