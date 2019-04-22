import random

from django.conf import settings

from web.games.base_game import BaseGame
from web.services.wallet import WalletService

class SpinGame(BaseGame):

    def __init__(self, user):
        self.bet_to_play = settings.MINIMUM_BET
        
        self.wallet_service = WalletService(user)
        self.bet_wallet = self.wallet_service.get_next_wallet_to_bet(self.bet_to_play)
        self.can_play = True if self.bet_wallet else False

    def play(self):
        won = True if random.randint(0,1) else False
        self.wallet_service.process_bet(self.bet_wallet, self.bet_to_play, won)
        return won
