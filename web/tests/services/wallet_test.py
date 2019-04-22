from decimal import Decimal

from django.test import TestCase

from web.services.wallet import WalletService
from web.models import Wallet, WalletTransaction


class WalletServiceCase(TestCase):

    fixtures = ['user.yaml']

    def test_deposit(self):
        wallet_service = WalletService(1)

        self.assertTrue(wallet_service.deposit(50.00))
        self.assertEquals(50.00, Wallet.objects.all()[0].amount)
        self.assertEquals(1, WalletTransaction.objects.count())
        self.assertEquals('deposit', WalletTransaction.objects.all()[0].action)

    def test_bonus(self):
        user_id = 1
        wallet_service = WalletService(user_id)
        bonus = wallet_service.bonus(amount=100.00,
                                     currency='BNS',
                                     wagering_requirement=20)
        
        updated_bns_wallet = Wallet.objects.filter(user=1, currency='BNS').first()

        self.assertTrue(bonus)
        self.assertEquals(100.00, updated_bns_wallet.amount)
        self.assertEquals(20, updated_bns_wallet.wagering_requirement)
        self.assertEquals(1, WalletTransaction.objects.filter(wallet=updated_bns_wallet.id).count())

    def test_eur_bonus(self):
        wallet_service = WalletService(1)
        bonus = wallet_service.bonus(amount=50.00,
                                     currency='EUR')

        updated_eur_wallet = Wallet.objects.filter(user=1, currency='EUR').first()

        self.assertTrue(bonus)
        self.assertEquals(50.00, updated_eur_wallet.amount)
        self.assertEquals(1, WalletTransaction.objects.filter(wallet=updated_eur_wallet.id).count())

    def test_has_amount_to_bet_at_eur_wallet(self):
        wallet = WalletService(2).get_next_wallet_to_bet(2.00)

        self.assertTrue(wallet)
        self.assertEquals('EUR', wallet.currency)

    def test_has_amount_to_bet_at_bns_wallet(self):
        wallet = WalletService(3).get_next_wallet_to_bet(2.00)

        self.assertTrue(wallet)
        self.assertEquals('BNS', wallet.currency)

    def test_user_bet_without_money_on_wallet(self):
        wallet = WalletService(1).get_next_wallet_to_bet(2.00)

        self.assertFalse(wallet)

    def test_user_with_bet_money_on_bns_and_eur_wallet(self):
        wallet = WalletService(4).get_next_wallet_to_bet(2.00)

        self.assertTrue(wallet)
        self.assertEquals('EUR', wallet.currency)

    def test_bet_won_on_eur_wallet(self):
        wallet_service = WalletService(2)
        bet_wallet = wallet_service.get_next_wallet_to_bet(2.00)
        self.assertTrue(wallet_service.process_bet(bet_wallet, 2.00, won=True))
        updated_wallet = Wallet.objects.filter(pk=bet_wallet.id).first()
        self.assertEquals(bet_wallet.amount + Decimal(2.00), updated_wallet.amount)
        self.assertEquals(2.00, updated_wallet.bet_amount)

    def test_bet_lose_on_eur_wallet(self):
        wallet_service = WalletService(2)
        bet_wallet = wallet_service.get_next_wallet_to_bet(2.00)
        self.assertTrue(wallet_service.process_bet(bet_wallet, 2.00, won=False))
        updated_wallet = Wallet.objects.filter(pk=bet_wallet.id).first()
        self.assertEquals(bet_wallet.amount - Decimal(2.00), updated_wallet.amount)
        self.assertEquals(2.00, updated_wallet.bet_amount)

    def test_bet_won_on_bns_wallet(self):
        wallet_service = WalletService(3)
        bet_wallet = wallet_service.get_next_wallet_to_bet(2.00)
        self.assertTrue(wallet_service.process_bet(bet_wallet, 2.00, won=True))
        updated_wallet = Wallet.objects.filter(pk=bet_wallet.id).first()
        self.assertEquals(bet_wallet.amount + Decimal(2.00), updated_wallet.amount)
        self.assertEquals(2.00, updated_wallet.bet_amount)
        self.assertEquals('BNS', updated_wallet.currency)

    def test_bet_lose_on_bns_wallet(self):
        wallet_service = WalletService(3)
        bet_wallet = wallet_service.get_next_wallet_to_bet(2.00)
        self.assertTrue(wallet_service.process_bet(bet_wallet, 2.00, won=False))
        updated_wallet = Wallet.objects.filter(pk=bet_wallet.id).first()
        self.assertEquals(bet_wallet.amount - Decimal(2.00), updated_wallet.amount)
        self.assertEquals(2.00, updated_wallet.bet_amount)
        self.assertEquals('BNS', updated_wallet.currency)




