from django.db import models

class ActionLog(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.UUIDField()
    user_email = models.EmailField()
