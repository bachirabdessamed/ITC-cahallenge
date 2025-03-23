# forms.py
from django import forms
from django.core.validators import MinValueValidator
from django import forms
from django.core.exceptions import ValidationError

class TransactionForm(forms.Form):
    recipient_account_number_suffix = forms.CharField(
        max_length=15,
        label="Recipient Account Number",
        help_text="Enter the part of the account number after 'ACCT-'"
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Amount",
        validators=[]
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password"
    )

    def clean_recipient_account_number_suffix(self):
        suffix = self.cleaned_data.get("recipient_account_number_suffix")
        if not suffix.isdigit():
            raise ValidationError("The account number suffix must be numeric.")
        return f"ACCT-{suffix}"

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is None or amount < 100:
            raise ValidationError("Amount must be at least 100.")
        return amount