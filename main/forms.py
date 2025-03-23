# forms.py
from django import forms

class TransactionForm(forms.Form):
    recipient_account_number = forms.CharField(max_length=20, label="Recipient Account Number")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
