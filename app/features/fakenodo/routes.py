"""HTTP routes that emulate the Zenodo deposit API.

Set ``ZENODO_API_URL=http://localhost:5000/fakenodo/api/deposit/depositions``
in your ``.env`` and the existing ``ZenodoService`` will talk to these
endpoints instead of the real Zenodo.

Supported contract (matches what ``zenodo/services.py`` actually calls):

    GET    /fakenodo/api/deposit/depositions            → list depositions
    POST   /fakenodo/api/deposit/depositions            → create a deposition
    GET    /fakenodo/api/deposit/depositions/<id>        → get a deposition
    DELETE /fakenodo/api/deposit/depositions/<id>        → delete a deposition
    PUT    /fakenodo/api/deposit/depositions/<id>        → update metadata
    POST   /fakenodo/api/deposit/depositions/<id>/files  → upload a file
    POST   /fakenodo/api/deposit/depositions/<id>/actions/publish    → publish
    POST   /fakenodo/api/deposit/depositions/<id>/actions/newversion → new version
"""

from flask import jsonify, request

from app.features.fakenodo import fakenodo_bp
from app.features.fakenodo.services import FakenodoService

API = "/fakenodo/api/deposit/depositions"


# ------------------------------------------------------------------
# List / Create
# ------------------------------------------------------------------


@fakenodo_bp.route(API, methods=["GET"])
def list_depositions():
    return jsonify(FakenodoService.list_depositions()), 200


@fakenodo_bp.route(API, methods=["POST"])
def create_deposition():
    body = request.get_json(silent=True) or {}
    metadata = body.get("metadata")
    dep = FakenodoService.create_deposition(metadata=metadata)
    return jsonify(dep), 201


# ------------------------------------------------------------------
# Single deposition
# ------------------------------------------------------------------


@fakenodo_bp.route(f"{API}/<int:dep_id>", methods=["GET"])
def get_deposition(dep_id):
    dep = FakenodoService.get_deposition(dep_id)
    if dep is None:
        return jsonify({"message": "Deposition not found"}), 404
    return jsonify(dep), 200


@fakenodo_bp.route(f"{API}/<int:dep_id>", methods=["DELETE"])
def delete_deposition(dep_id):
    if FakenodoService.delete_deposition(dep_id):
        return "", 204
    return jsonify({"message": "Deposition not found"}), 404


@fakenodo_bp.route(f"{API}/<int:dep_id>", methods=["PUT"])
def update_deposition(dep_id):
    body = request.get_json(silent=True) or {}
    metadata = body.get("metadata", {})
    dep = FakenodoService.update_metadata(dep_id, metadata)
    if dep is None:
        return jsonify({"message": "Deposition not found"}), 404
    return jsonify(dep), 200


# ------------------------------------------------------------------
# Files
# ------------------------------------------------------------------


@fakenodo_bp.route(f"{API}/<int:dep_id>/files", methods=["POST"])
def upload_file(dep_id):
    uploaded = request.files.get("file")
    name = request.form.get("name", "unnamed")
    content = uploaded.read() if uploaded else b""
    result = FakenodoService.upload_file(dep_id, name, content)
    if result is None:
        return jsonify({"message": "Deposition not found"}), 404
    return jsonify(result), 201


# ------------------------------------------------------------------
# Actions
# ------------------------------------------------------------------


@fakenodo_bp.route(f"{API}/<int:dep_id>/actions/publish", methods=["POST"])
def publish_deposition(dep_id):
    dep = FakenodoService.publish_deposition(dep_id)
    if dep is None:
        return jsonify({"message": "Deposition not found"}), 404
    return jsonify(dep), 202


@fakenodo_bp.route(f"{API}/<int:dep_id>/actions/newversion", methods=["POST"])
def new_version(dep_id):
    dep = FakenodoService.new_version(dep_id)
    if dep is None:
        return jsonify({"message": "Deposition not found"}), 404
    return jsonify(dep), 201


# ------------------------------------------------------------------
# Web view / Record preview
# ------------------------------------------------------------------


@fakenodo_bp.route("/fakenodo/records/<int:dep_id>", methods=["GET"])
def view_record(dep_id):
    dep = FakenodoService.get_deposition(dep_id)
    if dep is None:
        return jsonify({"message": "Record not found"}), 404
    return jsonify(dep), 200
