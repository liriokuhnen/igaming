from django.core.management.base import BaseCommand, CommandError

from web.models import Bonus

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        if not Bonus.objects.filter(bonus_type='DEPOSIT'):
            Bonus.objects.create(bonus_type='DEPOSIT',
                                 currency='BNS',
                                 value=20.00,
                                 wagering_requirement=10,
                                 minimum_deposit_value=100.00)
            self.stdout.write(self.style.SUCCESS('Deposit bonus is created with success'))
        else:
            self.stdout.write(self.style.SUCCESS('Deposit already created'))

        if not Bonus.objects.filter(bonus_type='LOGIN'):
            Bonus.objects.create(bonus_type='LOGIN',
                                 currency='EUR',
                                 value=100.00)
            self.stdout.write(self.style.SUCCESS('Login bonus is created with success'))
        else:
            self.stdout.write(self.style.SUCCESS('Login already created'))
