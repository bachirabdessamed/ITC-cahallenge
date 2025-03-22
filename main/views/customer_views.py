from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from main.decorators import restrict_access_if_pending_card, role_required
from main.models.bank_account import BankAccount
from main.models.bank_card import BankCard

from django.utils.timezone import now


@login_required
@role_required(allowed_roles=['CUSTOMER'])
def request_bank_card(request):
    if request.method == "POST":
        user = request.user

        # Check if the user already has a card in REQUESTED or APPROVED status
        existing_card = BankCard.objects.filter(user=user, status__in=["REQUESTED", "APPROVED"]).first()
        if existing_card:
            messages.error(request, "You already have a bank card in REQUESTED or APPROVED status.")
            return render(request, "request_bank_card.html")  # Render the same page with the alert

        # Proceed to create a new bank card request
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        new_card = BankCard.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            requested_at=now(),
        )

        messages.success(request, "Your bank card request has been submitted successfully.")
        return redirect("customer_home")  # Replace with the correct URL name

    return render(request, "request_bank_card.html")


@role_required(['CUSTOMER'])
@restrict_access_if_pending_card  # Restrict access if card status is "REQUESTED"
def money_account_view(request):
    user_bank_account = BankAccount.objects.filter(user=request.user).first()
    if not user_bank_account:
        return render(request, 'no_account.html')  # No account available
    return render(request, 'money_account.html', {'account': user_bank_account})

