import uuid
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render

from main.decorators import role_required
from main.models.bank_account import BankAccount
from main.models.bank_card import BankCard
from django.contrib.auth.decorators import login_required

from main.utils import log_action



@login_required
@role_required(allowed_roles=['BANK_WORKER'])
def manage_bank_cards(request):
    # Fetch all bank card requests with status "REQUESTED"
    card_requests = BankCard.objects.filter(status="REQUESTED")
    
    if request.method == "POST":
        # Handle card approval/rejection
        card_id = request.POST.get("card_id")
        action = request.POST.get("action")  # "approve" or "reject"
        
        try:
            bank_card = BankCard.objects.get(id=card_id)

            if action == "approve":
                # Generate a unique card number
                card_number = f"CARD-{uuid.uuid4().hex[:10].upper()}"  # Generate a 10-character card number
                bank_card.card_number = card_number  # Assign the generated card number
                bank_card.status = "APPROVED"
                
                # Create a bank account for the user
                from main.models.bank_account import BankAccount
                BankAccount.objects.create(
                    id=uuid.uuid4(),  # Generate a new UUID
                    user=bank_card.user,
                    account_number=f"ACCT-{bank_card.user.id:05d}",
                    balance=0.00
                )
                
                # Log the approval action
                log_action(
                    user=request.user,
                    action=f"Approved bank card request for user {bank_card.user.email}. Card number: {card_number}."
                )

            elif action == "reject":
                bank_card.status = "REJECTED"

                # Log the rejection action
                log_action(
                    user=request.user,
                    action=f"Rejected bank card request for user {bank_card.user.email}."
                )

            bank_card.save()

        except BankCard.DoesNotExist:
            # Log the failed attempt to act on a non-existent card
            log_action(
                user=request.user,
                action=f"Attempted to act on a non-existent bank card with ID {card_id}."
            )
    
        return redirect("manage_bank_cards")  # Reload page after action

    return render(request, "manage_bank_cards.html", {"card_requests": card_requests})


def generate_card_number():
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])

@login_required
@role_required(allowed_roles=['BANK_WORKER'])
def approve_bank_card(request, bank_card_id):
    if request.user.role != 'BANK_WORKER':
        messages.error(request, "You are not authorized to perform this action.")
        # Log unauthorized access attempt
        log_action(
            user=request.user,
            action=f"Unauthorized approval attempt for bank card ID {bank_card_id}."
        )
        return redirect('manage_bank_cards')

    bank_card = get_object_or_404(BankCard, id=bank_card_id)

    if bank_card.status == 'APPROVED':
        messages.warning(request, "This bank card request has already been approved.")
        # Log duplicate approval attempt
        log_action(
            user=request.user,
            action=f"Duplicate approval attempt for already approved bank card ID {bank_card_id}."
        )
        return redirect('manage_bank_cards')

    # Update the status to APPROVED
    bank_card.status = 'APPROVED'
    bank_card.save()

    # Generate a unique account number and create a new bank account
    account_number = str(uuid.uuid4().int)[:20]  # Generate a unique 20-digit account number
    BankAccount.objects.create(
        id=uuid.uuid4(),
        account_number=account_number,
        user=bank_card.user
    )

    # Log the approval and account creation action
    log_action(
        user=request.user,
        action=(
            f"Approved bank card request for user {bank_card.user.email}. "
            f"Account number {account_number} created."
        )
    )

    messages.success(
        request, 
        f"Bank card request approved, and a bank account has been created for {bank_card.user.username}."
    )
    return redirect('manage_bank_cards')