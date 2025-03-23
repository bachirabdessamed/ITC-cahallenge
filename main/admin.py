from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from main.models.notification import Notification
from main.models.user import User

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("user__username", "message")