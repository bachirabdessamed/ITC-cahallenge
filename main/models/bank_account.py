from django.db import models
from .user import User

class BankAccount(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
