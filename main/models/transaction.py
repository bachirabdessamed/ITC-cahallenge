from django.db import models
from .bank_account import BankAccount

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='sent_transactions')
    recipient_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='received_transactions')