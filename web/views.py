import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from web.games.spin import SpinGame
from web.services.account import AccountService
from web.services.wallet import WalletService
from web.services.bonus import BonusService
from web.forms import LoginForm, UserForm, DepositForm

logger = logging.getLogger(__name__)

def indexView(request):
    return render(request, 'index.html', {})


def signUpView(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            create_account = AccountService.CreateAccount(username, raw_password)
            messages.add_message(request, messages.INFO, 'Account created with success', 'alert-success')
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'sign_up.html', {'form': form})

def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                BonusService.bonus_login(user, request)
                return redirect('home')
            else:
                messages.add_message(request, messages.INFO, 'Invalid username or password', 'alert-danger')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logoutView(request):
    logout(request)
    return redirect('index')

@login_required()
def homeView(request):
    wallet_service = WalletService(request.user.id)
    return render(request, 'home.html', {'wallets': wallet_service.wallets})

@login_required()
def depositView(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount_deposit = form.cleaned_data.get('amount')
            WalletService(request.user.id).deposit(amount_deposit)
            BonusService.bonus_deposit(request.user.id, request, amount_deposit)
            messages.add_message(request, messages.INFO, 'Deposit successful', 'alert-success')
            return redirect('home')
        else:
            messages.add_message(request, messages.INFO, 'Invalid amount please deposit a value above than 0', 'alert-danger')

    else:
        form = DepositForm()

    return render(request, 'deposit.html', {'form': form})

@login_required()
def spinGameView(request):
    spin_game = SpinGame(request.user.id)
    bet_wallet = spin_game.bet_wallet
    game_is_played = False
    game_result = None
    bet_to_play = settings.MINIMUM_BET

    if request.method == 'POST':
        if spin_game.can_play:
            game_is_played = True
            game_result = spin_game.play()
        else:
            messages.add_message(request, messages.INFO, 'You dont have money to play', 'alert-danger')

    return render(request, 'spin_game.html', {'bet_wallet': bet_wallet,
                                              'game_is_played': game_is_played,
                                              'game_result': game_result,
                                              'bet_to_play': bet_to_play})
