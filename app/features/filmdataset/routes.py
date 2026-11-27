import uuid

from flask import abort, jsonify, make_response, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required

from app.features.dataset.services import DataSetService, DSDownloadRecordService
from app.features.filmdataset import filmdataset_bp
from app.features.filmdataset.forms import FilmdatasetForm
from app.features.filmdataset.services import FilmdatasetService

filmdataset_service = FilmdatasetService()
dataset_service = DataSetService()


@filmdataset_bp.route("/filmdataset", methods=["GET"])
def index():
    datasets = filmdataset_service.repository.latest_synchronized(limit=20)
    return render_template("filmdataset/index.html", datasets=datasets)


@filmdataset_bp.route("/filmdataset/upload", methods=["GET"])
@login_required
def create_filmdataset():
    return render_template("filmdataset/upload_filmdataset.html", form=FilmdatasetForm())


@filmdataset_bp.route("/filmdataset/upload", methods=["POST"])
@login_required
def upload_filmdataset():
    form = FilmdatasetForm()
    if not form.validate_on_submit():
        return jsonify({"message": form.errors}), 400

    result = filmdataset_service.upload_dataset(form=form, current_user=current_user)
    payload = {"message": result["message"]}
    if "dataset_id" in result:
        dataset_id = result["dataset_id"]
        payload["dataset_id"] = dataset_id
        dataset = filmdataset_service.get_or_404(dataset_id)
        if dataset.ds_meta_data.dataset_doi:
            payload["dataset_url"] = url_for("dataset.subdomain_index", doi=dataset.ds_meta_data.dataset_doi)
        else:
            payload["dataset_url"] = url_for("dataset.get_unsynchronized_dataset", dataset_id=dataset_id)
    return jsonify(payload), result["code"]


@filmdataset_bp.route("/filmdataset/file/upload", methods=["POST"])
@login_required
def upload_csv():
    result = filmdataset_service.save_temp_csv(request.files.get("file"), current_user)
    payload = {"message": result["message"]}
    for key in ("filename", "metrics", "errors"):
        if key in result:
            payload[key] = result[key]
    return jsonify(payload), result["code"]


@filmdataset_bp.route("/filmdataset/file/delete", methods=["POST"])
@login_required
def delete_csv():
    filename = (request.get_json() or {}).get("file")
    result = filmdataset_service.delete_temp_csv(filename, current_user)
    payload = {k: result[k] for k in ("message", "error") if k in result}
    return jsonify(payload), result["code"]


@filmdataset_bp.route("/filmdataset/<int:dataset_id>/preview", methods=["GET"])
def preview_filmdataset(dataset_id):
    dataset = filmdataset_service.get_or_404(dataset_id)
    if not dataset.ds_meta_data.dataset_doi and (
        not current_user.is_authenticated or current_user.id != dataset.user_id
    ):
        abort(404)

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=50, type=int)
    return jsonify(filmdataset_service.get_preview_rows(dataset, page=page, per_page=per_page)), 200


@filmdataset_bp.route("/filmdataset/download/<int:dataset_id>", methods=["GET"])
def download_filmdataset(dataset_id):
    dataset = filmdataset_service.get_or_404(dataset_id)
    tmp_dir, zip_name = dataset_service.build_download_archive(dataset)

    cookie = request.cookies.get("download_cookie") or str(uuid.uuid4())
    resp = make_response(send_from_directory(tmp_dir, zip_name, as_attachment=True, mimetype="application/zip"))
    if not request.cookies.get("download_cookie"):
        resp.set_cookie("download_cookie", cookie, max_age=60 * 60 * 24 * 365 * 2)

    DSDownloadRecordService().record_download(current_user, dataset_id, cookie)
    return resp
