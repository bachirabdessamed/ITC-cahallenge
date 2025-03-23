from datetime import timezone
from uuid import uuid4
from .models import ActionLog
from django.utils import timezone  # Correct import for timezone


def log_action(user, action, user_email=None):
    ActionLog.objects.create(
        user_id=user.id if user else uuid4(),  # Use a placeholder UUID
        user_email=user_email or (user.email if user else "unknown@example.com"),
        action=action,
        created_at=timezone.now(),
    )