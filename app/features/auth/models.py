from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db

# Role definitions for Role-Based Access Control (RBAC) - Issue #188
# - ROLE_USER: Standard authenticated user with basic platform permissions.
# - ROLE_CURATOR: Responsible for reviewing, curating and validating public film datasets.
# - ROLE_ADMIN: Full administrative privileges, user management and system settings.
ROLE_USER = "user"
ROLE_CURATOR = "curator"
ROLE_ADMIN = "admin"
ROLES = (ROLE_USER, ROLE_CURATOR, ROLE_ADMIN)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    role = db.Column(db.String(20), nullable=False, default=ROLE_USER, server_default=ROLE_USER)

    data_sets = db.relationship("DataSet", backref="user", lazy=True)
    profile = db.relationship("UserProfile", backref="user", uselist=False)

    def __init__(self, **kwargs):
        if "role" in kwargs:
            if kwargs["role"] not in ROLES:
                raise ValueError(f"Invalid role '{kwargs['role']}'. Must be one of {ROLES}.")
        else:
            kwargs["role"] = ROLE_USER

        super(User, self).__init__(**kwargs)
        if "password" in kwargs:
            self.set_password(kwargs["password"])

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self) -> bool:
        """Return True if the user has the 'admin' role."""
        return self.role == ROLE_ADMIN

    @property
    def is_curator(self) -> bool:
        """Return True if the user has the 'curator' role."""
        return self.role == ROLE_CURATOR

    def has_role(self, *roles: str) -> bool:
        """Check if the user holds at least one of the specified roles."""
        return self.role in roles

    def temp_folder(self) -> str:
        from app.features.auth.services import AuthenticationService

        return AuthenticationService().temp_folder_by_user(self)
