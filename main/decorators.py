from django.http import HttpResponseForbidden
from functools import wraps

from django.shortcuts import redirect

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return redirect('forbidden')  # Redirect to a forbidden page
        return _wrapped_view
    return decorator
