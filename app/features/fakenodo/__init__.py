from flask import Flask
from splent_framework.blueprints.base_blueprint import BaseBlueprint

fakenodo_bp = BaseBlueprint("fakenodo", __name__, template_folder="templates")


def init_feature(app: Flask) -> None:
    """Fakenodo needs no assets; the blueprint registers its routes on import."""
