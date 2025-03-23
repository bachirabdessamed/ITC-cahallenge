import logging
from celery import shared_task
from django.utils.timezone import now
from .models.notification import Notification
from .models.bank_account import BankAccount

logger = logging.getLogger(__name__)

@shared_task
def send_balance_notifications():
    low_balance_accounts = BankAccount.objects.filter(balance__lte=300)
    logger.info(f"Found {low_balance_accounts.count()} accounts with low balance.")
    
    for account in low_balance_accounts:
        logger.info(f"Creating notification for user {account.user.email} with balance {account.balance}.")
        Notification.objects.create(
            user=account.user,
            message=f"Your account balance is low ({account.balance} DZD). Please deposit funds.",
            created_at=now(),
        )
