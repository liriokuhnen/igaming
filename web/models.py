from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


CURRENCY_CHOICES = (
    ('EUR', 'Euro'),
    ('BNS', 'Bonus'),
)

class Wallet(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=00.00)
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2, default=00.00)
    wagering_requirement = models.IntegerField(default=0)
    bonus_initial = models.DecimalField(max_digits=10, decimal_places=2, default=00.00)
    depleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.currency

    def get_bonus_status(self):
        if self.currency == 'BNS':
            if self.bet_amount > (self.wagering_requirement * self.bonus_initial):
                return 'can withdrawn'
            return 'cannot withdraw'

class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    action = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

class Bonus(models.Model):

    class Meta:
        verbose_name_plural = 'bonuses'

    BONUS_TYPE = (
        ('LOGIN', 'login'),
        ('DEPOSIT', 'deposit'),
    )

    status = models.BooleanField(default=True)
    bonus_type = models.CharField(max_length=10, choices=BONUS_TYPE)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    wagering_requirement = models.IntegerField(default=0)
    minimum_deposit_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.bonus_type

    def clean(self):
        if self.currency == 'BNS':
            if not(self.wagering_requirement >= 1 and self.wagering_requirement <= 100):
                raise ValidationError("Wagering requirement to Bonus must be a value between 1 and 100")
