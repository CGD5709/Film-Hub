from flask import render_template
from app.features.filmdataset import filmdataset_bp


@filmdataset_bp.route('/filmdataset', methods=['GET'])
def index():
    return render_template('filmdataset/index.html')
