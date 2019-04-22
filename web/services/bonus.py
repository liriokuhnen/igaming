from django.contrib import messages

from web.models import Bonus
from web.services.wallet import WalletService


class BonusService(object):

    @classmethod
    def bonus_login(cls, user_id, request):
        all_bonus = Bonus.objects.filter(bonus_type='LOGIN', status=True).all()
        cls._process_bonus(all_bonus, user_id, request)

    @classmethod
    def bonus_deposit(cls, user_id, request, deposited_value):
        all_bonus = Bonus.objects.filter(bonus_type='DEPOSIT',
                                         status=True,
                                         minimum_deposit_value__lte=deposited_value).all()
        cls._process_bonus(all_bonus, user_id, request)

    @classmethod
    def _process_bonus(cls, all_bonus, user_id, request):
        if all_bonus:
            wallet_service = WalletService(user_id)

            for bonus in all_bonus:
                wallet_service.bonus(bonus.value, bonus.currency, bonus.wagering_requirement)
                msg = 'You win a bonus of {} - {}'.format(bonus.value, bonus.currency)
                messages.add_message(request, messages.INFO, msg, 'alert-success')
