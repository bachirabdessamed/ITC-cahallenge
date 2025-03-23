from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from main.decorators import restrict_access_if_pending_card, role_required
from main.models.bank_account import BankAccount
from main.models.bank_card import BankCard

from django.utils.timezone import now

from main.utils import log_action


@login_required
@role_required(allowed_roles=['CUSTOMER'])
def request_bank_card(request):
    if request.method == "POST":
        user = request.user

        # Check if the user already has a card in REQUESTED or APPROVED status
        existing_card = BankCard.objects.filter(user=user, status__in=["REQUESTED", "APPROVED"]).first()
        if existing_card:
            messages.error(request, "You already have a bank card in REQUESTED or APPROVED status.")
            
            # Log the attempt to request a duplicate card
            log_action(user, "Attempted to request a bank card while one is already in REQUESTED or APPROVED status.")
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

        # Log the successful bank card request
        log_action(user, f"Requested a new bank card for {first_name} {last_name} ({email}).")
        messages.success(request, "Your bank card request has been submitted successfully.")
        return redirect("customer_home")  # Replace with the correct URL name

    return render(request, "request_bank_card.html")


@role_required(['CUSTOMER'])
@restrict_access_if_pending_card  # Restrict access if card status is "REQUESTED"
def money_account_view(request):
    # Fetch the user's bank account
    user_bank_account = BankAccount.objects.filter(user=request.user).first()

    if not user_bank_account:
        # Log the missing account access attempt
        log_action(request.user, "Attempted to access money account but no account exists.")

        # Render a message or page for no account
        messages.error(request, "You do not have a bank account.")
        return render(request, 'no_account.html')  # No account available

    # Log successful account access
    log_action(request.user, f"Accessed money account with account number {user_bank_account.account_number}.")

    # Render the money account page
    return render(request, 'money_account.html', {'account': user_bank_account})

