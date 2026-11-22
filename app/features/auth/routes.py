from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from splent_framework.utils.form_helpers import form_error

from app import db
from app.features.auth import auth_bp
from app.features.auth.decorators import role_required
from app.features.auth.forms import LoginForm, SignupForm
from app.features.auth.models import ROLES, User
from app.features.auth.services import AuthenticationService
from app.features.profile.services import UserProfileService

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()


@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for("public.index"))

    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        if not authentication_service.is_email_available(email):
            return form_error("auth/signup_form.html", form, {"email": [f"{email} in use"]})

        user = authentication_service.create_with_profile(**form.data)
        login_user(user, remember=True)
        return redirect(url_for("public.index"))

    return render_template("auth/signup_form.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("public.index"))

    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        if authentication_service.login(form.email.data, form.password.data):
            return redirect(url_for("public.index"))
        return form_error("auth/login_form.html", form, {"credentials": ["Invalid credentials"]})

    return render_template("auth/login_form.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.index"))


@auth_bp.route("/admin/users", methods=["GET", "POST"])
@role_required("admin")
def admin_users():
    """Admin page to list registered users and modify their roles (Issue #188)."""
    if request.method == "POST":
        user_id = request.form.get("user_id", type=int)
        new_role = request.form.get("role")

        if not new_role or new_role not in ROLES:
            flash(f"Invalid role '{new_role}'. Must be one of {ROLES}.", "danger")
            return redirect(url_for("auth.admin_users"))

        target_user = User.query.get(user_id)
        if not target_user:
            flash(f"User with ID {user_id} not found.", "danger")
            return redirect(url_for("auth.admin_users"))

        if target_user.id == current_user.id and new_role != "admin":
            flash("You cannot remove your own admin role to prevent losing administrative access.", "warning")
            return redirect(url_for("auth.admin_users"))

        target_user.role = new_role
        db.session.commit()
        flash(f"Role of {target_user.email} updated to {new_role}.", "success")
        return redirect(url_for("auth.admin_users"))

    users = User.query.order_by(User.id.asc()).all()
    return render_template("auth/admin_users.html", users=users, available_roles=ROLES)
