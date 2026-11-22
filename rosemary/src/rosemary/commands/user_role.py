import click
from flask.cli import with_appcontext

from app import db
from app.features.auth.models import ROLE_ADMIN, ROLE_USER, ROLES, User


@click.command("user:promote", help="Promote a user to a specific role (default: admin).")
@click.argument("email")
@click.argument("role", default=ROLE_ADMIN)
@with_appcontext
def user_promote(email: str, role: str):
    """Promote a user to 'admin', 'curator', or another valid role."""
    role_norm = role.lower()
    if role_norm not in ROLES:
        click.echo(click.style(f"Error: Invalid role '{role}'. Must be one of {ROLES}.", fg="red"))
        raise click.Abort()

    user = User.query.filter_by(email=email).first()
    if not user:
        click.echo(click.style(f"Error: User with email '{email}' not found.", fg="red"))
        raise click.Abort()

    user.role = role_norm
    db.session.commit()
    click.echo(click.style(f"Successfully updated role of '{email}' to '{role_norm}'.", fg="green"))


@click.command("user:demote", help="Demote a user back to the default 'user' role.")
@click.argument("email")
@with_appcontext
def user_demote(email: str):
    """Demote a user back to the standard 'user' role."""
    user = User.query.filter_by(email=email).first()
    if not user:
        click.echo(click.style(f"Error: User with email '{email}' not found.", fg="red"))
        raise click.Abort()

    user.role = ROLE_USER
    db.session.commit()
    click.echo(click.style(f"Successfully demoted user '{email}' to role '{ROLE_USER}'.", fg="green"))
