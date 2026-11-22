"""Tests for role-based access control (RBAC), decorators, admin routes and CLI commands.

Issue #188: Admin roles (admin, curator, user).
"""

import pytest
from click.testing import CliRunner

from app import db
from app.features.auth.models import ROLES, User
from rosemary.commands.user_role import user_demote, user_promote

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# Unit tests: User Model Roles & Helpers
# ---------------------------------------------------------------------------


def test_user_default_role():
    """A new user without explicit role must have role='user' by default."""
    user = User(email="regular@example.com")
    assert user.role == "user"
    assert user.is_admin is False
    assert user.is_curator is False
    assert user.has_role("user") is True
    assert user.has_role("admin") is False
    assert user.has_role("curator") is False


def test_user_roles_properties():
    """Check is_admin, is_curator and has_role for each defined role."""
    admin = User(email="admin@example.com", role="admin")
    assert admin.role == "admin"
    assert admin.is_admin is True
    assert admin.is_curator is False
    assert admin.has_role("admin") is True
    assert admin.has_role("admin", "curator") is True
    assert admin.has_role("curator") is False

    curator = User(email="curator@example.com", role="curator")
    assert curator.role == "curator"
    assert curator.is_admin is False
    assert curator.is_curator is True
    assert curator.has_role("curator") is True
    assert curator.has_role("user") is False
    assert curator.has_role("admin", "curator") is True


def test_user_rejects_invalid_role():
    """Setting an invalid role raises ValueError."""
    with pytest.raises(ValueError):
        User(email="bad@example.com", role="superadmin")


# ---------------------------------------------------------------------------
# Integration tests: @role_required decorator & route protection
# ---------------------------------------------------------------------------


def test_role_required_blocks_anonymous_user(test_client):
    """Anonymous visitors are redirected to the login page when accessing protected routes."""
    test_client.get("/logout", follow_redirects=False)

    response = test_client.get("/admin/users", follow_redirects=False)
    assert response.status_code in (302, 303)
    assert "/login" in response.headers["Location"]

    response_zenodo = test_client.get("/zenodo/test", follow_redirects=False)
    assert response_zenodo.status_code in (302, 303)
    assert "/login" in response_zenodo.headers["Location"]


def test_role_required_blocks_standard_user(test_client):
    """Users with role='user' receive HTTP 403 on admin-only routes."""
    # Create and login as regular user
    user = User.query.filter_by(email="regular_user@example.com").first()
    if not user:
        user = User(email="regular_user@example.com", role="user")
        user.set_password("pass1234")
        db.session.add(user)
        db.session.commit()

    test_client.post("/login", data={"email": "regular_user@example.com", "password": "pass1234"})

    # Check /admin/users -> 403 Forbidden
    response_admin = test_client.get("/admin/users")
    assert response_admin.status_code == 403

    # Check /zenodo/test -> 403 Forbidden
    response_zenodo = test_client.get("/zenodo/test")
    assert response_zenodo.status_code == 403


def test_role_required_blocks_curator_from_admin_only(test_client):
    """Curators receive HTTP 403 when accessing routes restricted strictly to 'admin'."""
    curator = User.query.filter_by(email="curator_test@example.com").first()
    if not curator:
        curator = User(email="curator_test@example.com", role="curator")
        curator.set_password("pass1234")
        db.session.add(curator)
        db.session.commit()

    test_client.post("/login", data={"email": "curator_test@example.com", "password": "pass1234"})

    response_admin = test_client.get("/admin/users")
    assert response_admin.status_code == 403

    response_zenodo = test_client.get("/zenodo/test")
    assert response_zenodo.status_code == 403


def test_admin_can_access_admin_users_and_zenodo_test(test_client):
    """Admins can access /admin/users and /zenodo/test."""
    admin = User.query.filter_by(email="admin_test@example.com").first()
    if not admin:
        admin = User(email="admin_test@example.com", role="admin")
        admin.set_password("pass1234")
        db.session.add(admin)
        db.session.commit()

    test_client.post("/login", data={"email": "admin_test@example.com", "password": "pass1234"})

    response_admin = test_client.get("/admin/users")
    assert response_admin.status_code == 200
    assert b"admin_test@example.com" in response_admin.data

    response_zenodo = test_client.get("/zenodo/test")
    assert response_zenodo.status_code == 200


def test_admin_can_modify_user_role(test_client):
    """Admins can change a user's role via POST /admin/users."""
    target = User.query.filter_by(email="target_user@example.com").first()
    if not target:
        target = User(email="target_user@example.com", role="user")
        target.set_password("pass1234")
        db.session.add(target)
        db.session.commit()

    # Login as admin
    admin = User.query.filter_by(email="admin_test@example.com").first()
    if not admin:
        admin = User(email="admin_test@example.com", role="admin")
        admin.set_password("pass1234")
        db.session.add(admin)
        db.session.commit()

    test_client.post("/login", data={"email": "admin_test@example.com", "password": "pass1234"})

    # Promote target to curator
    response = test_client.post(
        "/admin/users",
        data={"user_id": target.id, "role": "curator"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    updated = User.query.get(target.id)
    assert updated.role == "curator"

    # Promote target to admin
    test_client.post(
        "/admin/users",
        data={"user_id": target.id, "role": "admin"},
        follow_redirects=True,
    )
    updated = User.query.get(target.id)
    assert updated.role == "admin"


def test_regular_user_cannot_modify_roles(test_client):
    """Non-admin users cannot POST to /admin/users."""
    regular = User.query.filter_by(email="regular_user@example.com").first()
    test_client.post("/login", data={"email": "regular_user@example.com", "password": "pass1234"})

    response = test_client.post(
        "/admin/users",
        data={"user_id": regular.id, "role": "admin"},
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# CLI tests: rosemary user:promote and user:demote
# ---------------------------------------------------------------------------


def test_rosemary_user_promote_and_demote_cli(test_app):
    """Rosemary CLI commands user:promote and user:demote work as expected."""
    runner = CliRunner()

    with test_app.app_context():
        # Ensure a test user exists
        user = User.query.filter_by(email="cli_test@example.com").first()
        if not user:
            user = User(email="cli_test@example.com", role="user")
            user.set_password("pass1234")
            db.session.add(user)
            db.session.commit()

        # Promote to admin
        res1 = runner.invoke(user_promote, ["cli_test@example.com", "admin"], obj=test_app)
        assert res1.exit_code == 0
        db.session.refresh(user)
        assert user.role == "admin"

        # Demote back to user
        res2 = runner.invoke(user_demote, ["cli_test@example.com"], obj=test_app)
        assert res2.exit_code == 0
        db.session.refresh(user)
        assert user.role == "user"

        # Promote to curator
        res3 = runner.invoke(user_promote, ["cli_test@example.com", "curator"], obj=test_app)
        assert res3.exit_code == 0
        db.session.refresh(user)
        assert user.role == "curator"

        # Promoting non-existent user exits with non-zero or error message
        res4 = runner.invoke(user_promote, ["nobody@example.com", "admin"], obj=test_app)
        assert res4.exit_code != 0 or "not found" in res4.output.lower()
