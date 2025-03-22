from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from main.models.bank_account import BankAccount
from main.models.transaction import Transaction

@login_required
def user_dashboard(request):
    if request.user.role != 'CUSTOMER':
        return HttpResponseForbidden("You are not authorized to view this page.")

    # Fetch user's bank account and transactions
    bank_accounts = BankAccount.objects.filter(user_id=request.user.id)
    transactions = Transaction.objects.filter(senderAccountID__user_id=request.user.id) | \
                   Transaction.objects.filter(recipeintAccountID__user_id=request.user.id)

    context = {
        'bank_accounts': bank_accounts,
        'transactions': transactions.order_by('-timestamp')[:10],  # Recent 10 transactions
    }
    return render(request, 'user_dashboard.html', context)
