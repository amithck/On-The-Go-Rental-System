from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from admin_app.models import admins


def is_admin_user(user):
    if not user or not user.is_authenticated:
        return False
    return admins.objects.filter(user=str(user)).exists()


def admin_required(view_func):
    @wraps(view_func)
    @login_required(login_url='/signin')
    def _wrapped(request, *args, **kwargs):
        if not is_admin_user(request.user):
            return redirect('/')
        return view_func(request, *args, **kwargs)

    return _wrapped
