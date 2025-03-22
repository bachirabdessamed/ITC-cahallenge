from django.contrib import messages

from django.shortcuts import redirect, render

from main.models.bank_card import BankCard
from django.contrib.auth.decorators import login_required



@login_required
def manage_bank_cards(request):
    if request.user.role != 'BANK_WORKER':
        return redirect('/login')

    bank_cards = BankCard.objects.filter(status='REQUESTED')

    if request.method == 'POST':
        card_id = request.POST['card_id']
        action = request.POST['action']  # "approve" or "reject"

        try:
            bank_card = BankCard.objects.get(id=card_id)
            if action == 'approve':
                bank_card.status = 'APPROVED'
                bank_card.card_number = generate_card_number()  # Function to generate card number
            elif action == 'reject':
                bank_card.status = 'REJECTED'
            bank_card.save()
            messages.success(request, f"Bank card request {action}d successfully.")
        except BankCard.DoesNotExist:
            messages.error(request, "Bank card request not found.")

    return render(request, 'manage_bank_cards.html', {'bank_cards': bank_cards})


def generate_card_number():
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(16)])
