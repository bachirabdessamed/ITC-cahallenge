from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('CUSTOMER', 'Customer'),
        ('ADMIN', 'Admin'),
        ('BANK_WORKER', 'Bank Worker'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')

    # Resolve the reverse accessor conflict
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Add a unique related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Add a unique related_name
        blank=True,
    )
