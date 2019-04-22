from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from web.services.account import AccountService


class UserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password again'
    }))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

class DepositForm(forms.Form):
    amount = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '00.00'
    }))

    def convert_string_to_float(self, string):
        return float(string.replace('.', '').replace(',', '.'))

    def clean(self):
        cleaned_data = self.cleaned_data
        amount = self.convert_string_to_float(cleaned_data['amount'])

        if amount <= 0:
            raise ValidationError("Amount can't be less than 0")

        cleaned_data['amount'] = amount
        return cleaned_data
