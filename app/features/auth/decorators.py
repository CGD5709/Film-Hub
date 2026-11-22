from functools import wraps

from flask import abort, redirect, request, url_for
from flask_login import current_user


def role_required(*roles: str):
    """Decorator to restrict access to authenticated users having one of the specified roles.

    - Unauthenticated visitors are redirected to the login page.
    - Authenticated users lacking the required role receive HTTP 403 Forbidden.

    Usage:
        @role_required("admin")
        def admin_view(): ...

        @role_required("admin", "curator")
        def curator_view(): ...
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login", next=request.url))
            if not current_user.has_role(*roles):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    """Shortcut decorator for routes restricted to 'admin' users."""
    return role_required("admin")(f)
