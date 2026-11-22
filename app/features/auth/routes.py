from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from splent_framework.utils.form_helpers import form_error

from app.features.auth import auth_bp
from app.features.auth.decorators import role_required
from app.features.auth.forms import LoginForm, RoleUpdateForm, SignupForm
from app.features.auth.models import ROLES
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
    form = RoleUpdateForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user_id = int(form.user_id.data)
            except (ValueError, TypeError):
                flash("Invalid user ID.", "danger")
                return redirect(url_for("auth.admin_users"))

            new_role = form.role.data

            target_user = authentication_service.get_by_id(user_id)
            if not target_user:
                flash(f"User with ID {user_id} not found.", "danger")
                return redirect(url_for("auth.admin_users"))

            if target_user.id == current_user.id and new_role != "admin":
                flash("You cannot remove your own admin role to prevent losing administrative access.", "warning")
                return redirect(url_for("auth.admin_users"))

            authentication_service.update_role(target_user, new_role)
            flash(f"Role of {target_user.email} updated to {new_role}.", "success")
            return redirect(url_for("auth.admin_users"))

        flash(f"Invalid form submission or role. Must be one of {ROLES}.", "danger")
        return redirect(url_for("auth.admin_users"))

    users = authentication_service.get_all_users()
    return render_template("auth/admin_users.html", users=users, available_roles=ROLES, form=form)
