# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.models import Notification

@login_required
def notifications_view(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notifications.html", {"notifications": user_notifications})
