# Generated by Django 2.2 on 2019-04-22 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('bonus_type', models.CharField(choices=[('LOGIN', 'login'), ('DEPOSIT', 'deposit')], max_length=10)),
                ('currency', models.CharField(choices=[('EUR', 'Euro'), ('BNS', 'Bonus')], max_length=3)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('wagering_requirement', models.IntegerField(default=0)),
                ('minimum_deposit_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('EUR', 'Euro'), ('BNS', 'Bonus')], max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('bet_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('wagering_requirement', models.IntegerField(default=0)),
                ('bonus_initial', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('depleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Wallet')),
            ],
        ),
    ]
