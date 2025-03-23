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

from main.utils import log_action


@login_required
@role_required(allowed_roles=['CUSTOMER'])
def transfer_money(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            recipient_account_number = form.cleaned_data['recipient_account_number_suffix']
            amount = form.cleaned_data['amount']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(username=request.user.username, password=password)
            if not user:
                messages.error(request, "Invalid password.")
                log_action(request.user, "Failed money transfer due to invalid password.")
                return redirect('transfer_money')

            # Get sender's bank account
            try:
                sender_account = BankAccount.objects.get(user=request.user)
            except BankAccount.DoesNotExist:
                messages.error(request, "You don't have a bank account.")
                log_action(request.user, "Failed money transfer: No bank account found.")
                return redirect('transfer_money')

            # Check if the recipient's account number matches the sender's
            if sender_account.account_number == recipient_account_number:
                messages.error(request, "You cannot transfer money to your own account.")
                log_action(request.user, "Failed money transfer: Attempted transfer to own account.")
                return redirect('transfer_money')

            # Check if the sender has enough balance
            if sender_account.balance < amount:
                messages.error(request, "Insufficient balance.")
                log_action(request.user, f"Failed money transfer: Insufficient balance. Attempted to transfer {amount}.")
                return redirect('transfer_money')

            # Get the recipient's bank account
            try:
                recipient_account = BankAccount.objects.get(account_number=recipient_account_number)
            except BankAccount.DoesNotExist:
                messages.error(request, "Recipient account not found.")
                log_action(request.user, f"Failed money transfer: Recipient account '{recipient_account_number}' not found.")
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

            # Log the successful transaction
            log_action(request.user, f"Successfully transferred {amount} to account {recipient_account_number}.")
            messages.success(request, "Transaction completed successfully.")
            return redirect('transfer_money')
    else:
        form = TransactionForm()

    # Pass sender's account number to the template
    try:
        sender_account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        sender_account = None

    return render(request, 'transfer_money.html', {'form': form, 'sender_account': sender_account})