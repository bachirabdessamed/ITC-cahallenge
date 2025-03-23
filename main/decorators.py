from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect

from main.models.bank_card import BankCard

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect('forbidden')  # Redirect to a forbidden page
        return _wrapped_view
    return decorator

def restrict_access_if_pending_card(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'CUSTOMER':
            has_pending_card = BankCard.objects.filter(user=request.user, status='REQUESTED').exists()
            if has_pending_card:
                return HttpResponseForbidden("You cannot access this page while your bank card request is pending.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('customer_home')  # Replace 'customer_home' with the desired redirect page
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func