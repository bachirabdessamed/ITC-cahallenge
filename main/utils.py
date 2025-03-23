from uuid import uuid4
from .models import ActionLog

def log_action(user, action):
    """
    Logs an action performed by a user.

    Args:
        user: The user performing the action (Django User object).
        action: A string describing the action.
    """
    ActionLog.objects.create(
        id=uuid4(),
        action=action,
        user_id=user.id,
        user_email=user.email
    )