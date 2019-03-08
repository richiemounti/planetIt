import threading
from functools import wraps
from threading import Thread
from app.models import Permission
from flask import abort
from flask_login import current_user


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

def demo_admin_required(f):
    return permission_required(Permission.DEMO_ADMINISTER)(f)



