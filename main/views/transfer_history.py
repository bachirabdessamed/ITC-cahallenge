from django.shortcuts import render
from main.decorators import role_required
from main.models.bank_account import BankAccount
from django.contrib.auth.decorators import login_required


@login_required
@role_required(allowed_roles=['CUSTOMER'])
def transfer_history(request):
    try:
        bank_account = BankAccount.objects.get(user=request.user)
        sent_transactions = bank_account.sent_transactions.all()
        received_transactions = bank_account.received_transactions.all()
    except BankAccount.DoesNotExist:
        sent_transactions = []
        received_transactions = []

    return render(request, 'transfer_history.html', {
        'sent_transactions': sent_transactions,
        'received_transactions': received_transactions
    })
