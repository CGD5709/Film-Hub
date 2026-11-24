"""In-memory storage for the fake Zenodo service.

No database is involved: depositions live in a plain dictionary that is
reset whenever the process restarts. This is intentional — fakenodo exists
only for development and integration testing.
"""

from app import db


class Fakenodo(db.Model):
    """Placeholder model so splent_framework's feature loader does not complain.

    The real storage is the in-memory dict managed by
    ``fakenodo.services.FakenodoService``.
    """

    id = db.Column(db.Integer, primary_key=True)
