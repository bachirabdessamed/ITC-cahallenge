# views.py
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from uuid import uuid4

from main.decorators import role_required
from main.forms import TransactionForm
from main.models.bank_account import BankAccount
from main.models.transaction import Transaction
from django.contrib.auth.decorators import login_required


@login_required
@role_required(allowed_roles=['CUSTOMER'])
def transfer_money(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            recipient_account_number = form.cleaned_data['recipient_account_number']
            amount = form.cleaned_data['amount']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(username=request.user.username, password=password)
            if not user:
                messages.error(request, "Invalid password.")
                return redirect('transfer_money')

            # Get sender's bank account
            try:
                sender_account = BankAccount.objects.get(user=request.user)
            except BankAccount.DoesNotExist:
                messages.error(request, "You don't have a bank account.")
                return redirect('transfer_money')

            # Check if the sender has enough balance
            if sender_account.balance < amount:
                messages.error(request, "Insufficient balance.")
                return redirect('transfer_money')

            # Get the recipient's bank account
            try:
                recipient_account = BankAccount.objects.get(account_number=recipient_account_number)
            except BankAccount.DoesNotExist:
                messages.error(request, "Recipient account not found.")
                return redirect('transfer_money')

            # Perform the transaction
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()

            # Save the transaction record
            Transaction.objects.create(
                id=uuid4(),
                amount=amount,
                sender_account=sender_account,
                recipient_account=recipient_account
            )

            messages.success(request, "Transaction completed successfully.")
            return redirect('transfer_money')
    else:
        form = TransactionForm()

    return render(request, 'transfer_money.html', {'form': form})
