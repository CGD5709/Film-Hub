"""Tests for role-based access control (RBAC), decorators, admin routes and CLI commands.

Issue #188: Admin roles (admin, curator, user).
"""

from unittest.mock import patch

import pytest
from click.testing import CliRunner
from flask import jsonify

from app import db
from app.features.auth.models import User
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


def test_role_required_blocks_standard_user(test_client, test_app):
    """Users with role='user' receive HTTP 403 on admin-only routes."""
    with test_app.app_context():
        user = User.query.filter_by(email="regular_user@example.com").first()
        if not user:
            user = User(email="regular_user@example.com", role="user")
            user.set_password("pass1234")
            db.session.add(user)
            db.session.commit()

    test_client.post("/login", data={"email": "regular_user@example.com", "password": "pass1234"})

    # Check /admin/users -> 403 Forbidden with custom 403.html template
    response_admin = test_client.get("/admin/users")
    assert response_admin.status_code == 403
    assert b"Forbidden" in response_admin.data
    assert b"403" in response_admin.data

    # Check /zenodo/test -> 403 Forbidden with custom 403.html template
    response_zenodo = test_client.get("/zenodo/test")
    assert response_zenodo.status_code == 403
    assert b"Forbidden" in response_zenodo.data
    assert b"403" in response_zenodo.data


def test_role_required_blocks_curator_from_admin_only(test_client, test_app):
    """Curators receive HTTP 403 when accessing routes restricted strictly to 'admin'."""
    with test_app.app_context():
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


def test_admin_can_access_admin_users_and_zenodo_test(test_client, test_app):
    """Admins can access /admin/users and /zenodo/test."""
    with test_app.app_context():
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

    with patch(
        "app.features.zenodo.services.ZenodoService.test_full_connection",
        return_value=jsonify({"success": True}),
    ):
        response_zenodo = test_client.get("/zenodo/test")
        assert response_zenodo.status_code == 200


def test_admin_can_modify_user_role(test_client, test_app):
    """Admins can change a user's role via POST /admin/users."""
    with test_app.app_context():
        target = User.query.filter_by(email="target_user@example.com").first()
        if not target:
            target = User(email="target_user@example.com", role="user")
            target.set_password("pass1234")
            db.session.add(target)
            db.session.commit()
        target_id = target.id

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
        data={"user_id": target_id, "role": "curator"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    with test_app.app_context():
        updated = User.query.get(target_id)
        assert updated.role == "curator"

    # Promote target to admin
    test_client.post(
        "/admin/users",
        data={"user_id": target_id, "role": "admin"},
        follow_redirects=True,
    )
    with test_app.app_context():
        updated = User.query.get(target_id)
        assert updated.role == "admin"


def test_admin_cannot_demote_themselves(test_client, test_app):
    """An admin user cannot remove their own admin role via /admin/users."""
    with test_app.app_context():
        admin = User.query.filter_by(email="self_admin@example.com").first()
        if not admin:
            admin = User(email="self_admin@example.com", role="admin")
            admin.set_password("pass1234")
            db.session.add(admin)
            db.session.commit()
        admin_id = admin.id

    test_client.post("/login", data={"email": "self_admin@example.com", "password": "pass1234"})

    # Attempt self-demotion to user
    response = test_client.post(
        "/admin/users",
        data={"user_id": admin_id, "role": "user"},
        follow_redirects=True,
    )
    # The response must remain 200 (not 403 Forbidden) and user must remain admin
    assert response.status_code == 200

    with test_app.app_context():
        reloaded = User.query.get(admin_id)
        assert reloaded.role == "admin"
        assert reloaded.is_admin is True


def test_regular_user_cannot_modify_roles(test_client, test_app):
    """Non-admin users cannot POST to /admin/users."""
    with test_app.app_context():
        regular = User.query.filter_by(email="regular_user@example.com").first()
        if not regular:
            regular = User(email="regular_user@example.com", role="user")
            regular.set_password("pass1234")
            db.session.add(regular)
            db.session.commit()
        regular_id = regular.id

    test_client.post("/login", data={"email": "regular_user@example.com", "password": "pass1234"})

    response = test_client.post(
        "/admin/users",
        data={"user_id": regular_id, "role": "admin"},
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


def test_rosemary_user_promote_invalid_role_cli(test_app):
    """Promoting with an invalid role via CLI aborts with error message."""
    runner = CliRunner()
    res = runner.invoke(user_promote, ["cli_test@example.com", "superhero"], obj=test_app)
    assert res.exit_code != 0
    assert "invalid role" in res.output.lower()


def test_role_required_multiple_roles_curator_and_admin(test_app, test_client):
    """Test routes protected by @role_required('admin', 'curator') via /curator/test."""
    # 1. Anonymous -> redirect to login
    test_client.get("/logout")
    res_anon = test_client.get("/curator/test")
    assert res_anon.status_code in (302, 303)
    assert "/login" in res_anon.headers["Location"]

    # 2. Regular user -> 403 Forbidden with custom 403.html template
    with test_app.app_context():
        user = User.query.filter_by(email="regular_for_multirole@example.com").first()
        if not user:
            user = User(email="regular_for_multirole@example.com", role="user")
            user.set_password("pass1234")
            db.session.add(user)
            db.session.commit()

    test_client.post("/login", data={"email": "regular_for_multirole@example.com", "password": "pass1234"})
    res_user = test_client.get("/curator/test")
    assert res_user.status_code == 403
    assert b"Forbidden" in res_user.data
    assert b"403" in res_user.data

    # 3. Curator -> 200 OK
    test_client.get("/logout")
    with test_app.app_context():
        curator = User.query.filter_by(email="curator_for_multirole@example.com").first()
        if not curator:
            curator = User(email="curator_for_multirole@example.com", role="curator")
            curator.set_password("pass1234")
            db.session.add(curator)
            db.session.commit()

    test_client.post("/login", data={"email": "curator_for_multirole@example.com", "password": "pass1234"})
    res_curator = test_client.get("/curator/test")
    assert res_curator.status_code == 200
    assert b"OK Curator" in res_curator.data

    # 4. Admin -> 200 OK
    test_client.get("/logout")
    with test_app.app_context():
        admin = User.query.filter_by(email="admin_for_multirole@example.com").first()
        if not admin:
            admin = User(email="admin_for_multirole@example.com", role="admin")
            admin.set_password("pass1234")
            db.session.add(admin)
            db.session.commit()

    test_client.post("/login", data={"email": "admin_for_multirole@example.com", "password": "pass1234"})
    res_admin = test_client.get("/curator/test")
    assert res_admin.status_code == 200
    assert b"OK Curator" in res_admin.data


def test_admin_required_decorator(test_app, test_client):
    """Test routes protected by @admin_required via /zenodo/test."""
    with test_app.app_context():
        mock_response = jsonify({"success": True})
        for email, role in [
            ("regular_for_adminreq@example.com", "user"),
            ("curator_for_adminreq@example.com", "curator"),
            ("admin_for_adminreq@example.com", "admin"),
        ]:
            u = User.query.filter_by(email=email).first()
            if not u:
                u = User(email=email, role=role)
                u.set_password("pass1234")
                db.session.add(u)
        db.session.commit()

    with patch(
        "app.features.zenodo.services.ZenodoService.test_full_connection",
        return_value=mock_response,
    ):
        # User -> 403
        test_client.get("/logout")
        test_client.post("/login", data={"email": "regular_for_adminreq@example.com", "password": "pass1234"})
        res_user = test_client.get("/zenodo/test")
        assert res_user.status_code == 403
        assert b"Forbidden" in res_user.data

        # Curator -> 403
        test_client.get("/logout")
        test_client.post("/login", data={"email": "curator_for_adminreq@example.com", "password": "pass1234"})
        res_curator = test_client.get("/zenodo/test")
        assert res_curator.status_code == 403
        assert b"Forbidden" in res_curator.data

        # Admin -> 200
        test_client.get("/logout")
        test_client.post("/login", data={"email": "admin_for_adminreq@example.com", "password": "pass1234"})
        res_admin = test_client.get("/zenodo/test")
        assert res_admin.status_code == 200


def test_admin_users_post_error_handling(test_client, test_app):
    """POST /admin/users handles invalid users or invalid roles cleanly."""
    with test_app.app_context():
        admin = User.query.filter_by(email="admin_test@example.com").first()
        if not admin:
            admin = User(email="admin_test@example.com", role="admin")
            admin.set_password("pass1234")
            db.session.add(admin)
            db.session.commit()
        admin_id = admin.id

    test_client.post("/login", data={"email": "admin_test@example.com", "password": "pass1234"})

    # 1. Non-existent user ID
    res_nonexistent = test_client.post(
        "/admin/users",
        data={"user_id": 99999, "role": "curator"},
        follow_redirects=True,
    )
    assert res_nonexistent.status_code == 200
    assert b"not found" in res_nonexistent.data.lower()

    # 2. Invalid role
    res_invalid_role = test_client.post(
        "/admin/users",
        data={"user_id": admin_id, "role": "superadmin"},
        follow_redirects=True,
    )
    assert res_invalid_role.status_code == 200
    assert b"invalid" in res_invalid_role.data.lower()
