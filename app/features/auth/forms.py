from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import AnyOf, DataRequired, Email, Length, Regexp

from app.features.auth.models import ROLES


class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    surname = StringField("Surname", validators=[DataRequired(), Length(max=100)])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")


class RoleUpdateForm(FlaskForm):
    user_id = HiddenField(
        "User ID",
        validators=[
            DataRequired(),
            Regexp(r"^\d+$", message="User ID must be a numeric integer."),
        ],
    )
    role = SelectField(
        "Role",
        choices=[(r, r) for r in ROLES],
        validators=[DataRequired(), AnyOf(ROLES, message=f"Role must be one of {ROLES}.")],
    )
    submit = SubmitField("Update")
