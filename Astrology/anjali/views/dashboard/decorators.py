from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        if not request.user.is_superuser:
            messages.error(request, "Aapke paas dashboard access nahi hai.")
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped
